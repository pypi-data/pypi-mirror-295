from __future__ import annotations

from typing import TYPE_CHECKING

from aio_client.provider.api import push_request
from aio_client.provider.models import PostProviderRequest
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery

from kinder.core.children.models import ChildrenDelegate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationUnit

from concentrator.smev3_v321.base.utils import get_adaptation_program
from concentrator.smev3_v321.base.utils import get_address
from concentrator.smev3_v321.base.utils import get_child_info
from concentrator.smev3_v321.base.utils import get_language
from concentrator.smev3_v321.base.utils import get_medical_report_without_files
from concentrator.smev3_v321.base.utils import get_person_identity_doc_info
from concentrator.smev3_v321.base.utils import get_person_info
from concentrator.smev3_v321.base.utils import get_schedule
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import PRIVILEGE_DOC_ISSUED
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.enums import StatusCode
from concentrator.smev3_v321.exceptions import ContentFailure
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.models import DeclarationOriginMessageID
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)


if TYPE_CHECKING:
    from django.db.models import QuerySet

    from concentrator.smev3_v321.model import FormDataMessage


class GetApplicationRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса GetApplicationRequest."""

    name_service: str = 'GetApplicationRequest'
    service_type_name: str = kinder_conc.GetApplicationRequestType.__name__

    @classmethod
    def prepare_query(cls) -> QuerySet:
        """Выполняет подготовку запроса."""

        subquery_first_delegate = (
            ChildrenDelegate.objects.filter(
                id=Subquery(
                    ChildrenDelegate.objects.filter(
                        children_id=OuterRef('children_id')
                    ).order_by('id').values('id')[:1])
            ).select_related('delegate'))

        subquery_declaration_units = (
            DeclarationUnit.objects.select_related('unit', 'sibling').only(
                'unit__name', 'unit_id', 'ord', 'declaration_id', 'sibling'))

        query = (
            Declaration.objects.select_related(
                'children'
            ).prefetch_related(
                Prefetch('declarationunit_set',
                         queryset=subquery_declaration_units,
                         to_attr='declaration_units')
            ).prefetch_related(
                Prefetch('children__childrendelegate_set',
                         queryset=subquery_first_delegate,
                         to_attr='first_childrendelegate')
            )
        )

        return query

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs) -> ExecutionData:

        request = message.parse_body.GetApplicationRequest

        declaration, is_portal = get_declaration_by_client_or_portal_id(
            cls.prepare_query(), request.orderId)

        content_failure_comment = None

        try:
            response_body = render_type2xml(
                cls.get_response(request, declaration),
                name_type='FormDataResponse'
            )
        except ContentFailure as exc:
            response_body = render_type2xml(
                kinder_conc.FormDataResponseType(
                    changeOrderInfo=kinder_conc.changeOrderInfoType(
                        orderId=kinder_conc.orderIdType(request.orderId),
                        statusCode=kinder_conc.statusCodeType(
                            exc.content_failure_code),
                        comment=exc.content_failure_comment)),
                name_type='FormDataResponse')
            content_failure_comment = exc.content_failure_comment

        # Для заявлений, найденных через связь с DeclarationPortalID, создаются
        # записи в DeclarationOriginMessageID (если таковых нет) для отправки
        # в дальнейшем информации о статусе заявления периодической задачей
        # DirectStatusCheckPeriodicAsyncTask
        if declaration and is_portal:
            domid, created = DeclarationOriginMessageID.objects.get_or_create(
                declaration_id=declaration.id)
            if created:
                domid.message_id = message.origin_message_id
                domid.replay_to = message.replay_to
                domid.save()

        response = push_request(PostProviderRequest(
            origin_message_id=message.origin_message_id,
            body=response_body,
            message_type=message.message_type,
            replay_to=message.replay_to,
            is_test_message=message.is_test_message))

        return ExecutionData(
            response,
            {
                'method_name': cls.name_service,
                'response': response_body,
                'result': content_failure_comment or SUCCESS_MESSAGE
            })

    @classmethod
    def get_response(
            cls,
            request: kinder_conc.GetApplicationRequestType,
            declaration: Declaration
    ) -> kinder_conc.FormDataResponseType:
        """Формирует ответ на GetApplicationRequest.

        :param request: Сгенерированное тело запроса.
        :param declaration: Заявление.

        :return: Тело ответа.

        :raise: ContentFailure

        """

        if not declaration:
            raise ContentFailure(
                StatusCode.CODE_150.value,
                'Заявление по указанным параметрам не найдено')

        child = declaration.children
        children_delegate, *_ = (
            declaration.children.first_childrendelegate or (None,))

        if not children_delegate:
            raise ContentFailure(
                StatusCode.CODE_150.value, 'Не найден представитель')

        delegate = children_delegate.delegate

        entry_params = kinder_conc.EntryParamsType(
            EntryDate=declaration.desired_date,
            Language=kinder_conc.DataElementType(
                **get_language(declaration.spec)),
            Schedule=kinder_conc.DataElementType(
                **get_schedule(declaration.work_type)),
            AgreementOnFullDayGroup=declaration.consent_full_time_group,
        )

        edu_org_info = kinder_conc.EduOrganizationsType(
            AllowOfferOther=declaration.offer_other)
        all_declaration_units = declaration.declaration_units

        for declaration_unit in all_declaration_units:
            edu_org_info.add_EduOrganization(
                kinder_conc.EduOrganizationType(
                    code=declaration_unit.unit_id,
                    PriorityNumber=declaration_unit.ord,
                    valueOf_=declaration_unit.unit.name,
                )
            )

        app_type = kinder_conc.GetApplicationResponseType(
            orderId=request.orderId,
            PersonInfo=get_person_info(kinder_conc, delegate),
            PersonIdentityDocInfo=(
                get_person_identity_doc_info(
                    kinder_conc, delegate, declaration)),
            ChildInfo=get_child_info(kinder_conc, declaration),
            Address=get_address(kinder_conc, child),
            EntryParams=entry_params,
            AdaptationProgram=get_adaptation_program(kinder_conc, declaration),
            MedicalReport=get_medical_report_without_files(
                kinder_conc, declaration),
            EduOrganizations=edu_org_info)

        declaration_privilege = DeclarationPrivilege.objects.filter(
            privilege=declaration.best_privilege, declaration=declaration,
            privilege__esnsi_code__isnull=False
        ).first()

        if declaration_privilege:

            doc_expiration_date = {}
            if declaration_privilege._privilege_end_date:
                doc_expiration_date['DocExpirationDate'] = (
                    declaration_privilege._privilege_end_date)

            benefit_doc_info = kinder_conc.DocInfoType(
                DocIssueDate=(
                    declaration_privilege.doc_date or declaration.date),
                DocIssued=(
                    declaration_privilege.doc_issued_by
                    or PRIVILEGE_DOC_ISSUED),
                **doc_expiration_date)

            app_type.set_BenefitInfo(
                kinder_conc.BenefitInfoWithoutFilesType(
                    BenefitCategory=kinder_conc.DataElementType(
                        code=declaration_privilege.privilege.esnsi_code,
                        valueOf_=declaration_privilege.privilege.name,
                    ),
                    BenefitDocInfo=benefit_doc_info
                )
            )

        for declaration_unit in all_declaration_units:
            if declaration_unit.sibling:
                app_type.add_BrotherSisterInfo(
                    kinder_conc.BrotherSisterInfoType(
                        ChildSurname=declaration_unit.sibling.surname,
                        ChildName=declaration_unit.sibling.firstname,
                        ChildMiddleName=declaration_unit.sibling.patronymic,
                        EduOrganization=kinder_conc.DataElementType(
                            code=declaration_unit.unit_id,
                            valueOf_=declaration_unit.unit.name,
                        ),
                    )
                )

        response = kinder_conc.FormDataResponseType(
            GetApplicationResponse=app_type)

        return response
