from __future__ import annotations

from typing import TYPE_CHECKING

from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from django.core.cache import cache

from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatus

from concentrator.smev3_v321.base.utils import is_cancel_allowed
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import CACHE_REJECTED_WITH_CANCEL_REQUEST
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.enums import StatusCode
from concentrator.smev3_v321.exceptions import ContentFailure
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)

from .constants import CANCEL_SUCCESS_COMMENT
from .constants import DECL_CANT_REJECTED
from .constants import DECL_NOT_FOUND
from .constants import WHY_CHANGE


if TYPE_CHECKING:
    from concentrator.smev3_v321.model import FormDataMessage


class CancelRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса cancelRequest."""

    name_service: str = 'cancelRequest'
    service_type_name: str = kinder_conc.cancelRequestType.__name__

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs) -> ExecutionData:

        request = message.parse_body.cancelRequest

        content_failure_comment = None

        try:
            response_body = render_type2xml(
                cls.get_response(request), name_type='FormDataResponse')
        except ContentFailure as exc:
            response_body = render_type2xml(
                kinder_conc.FormDataResponseType(
                    changeOrderInfo=kinder_conc.changeOrderInfoType(
                        orderId=kinder_conc.orderIdType(request.orderId),
                        statusCode=kinder_conc.statusCodeType(
                            StatusCode.CODE_150.value),
                        comment=exc.content_failure_comment)),
                name_type='FormDataResponse')
            content_failure_comment = exc.content_failure_comment

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
            cls, request: kinder_conc.cancelRequestType
    ) -> kinder_conc.FormDataResponseType:
        """Формирует ответ на cancelRequest.

        :param request: Запрос на отмену заявления.

        :return: Ответ на запрос cancelRequest

        :raise: ContentFailure

        """

        declaration, _ = get_declaration_by_client_or_portal_id(
            Declaration.objects.select_related('status'), request.orderId)

        if not declaration:
            raise ContentFailure(
                kinder_conc.CancelResultType.REJECTED, DECL_NOT_FOUND)
        elif (
                declaration.status.code in (
                    DSS.no_active_statuses(), DSS.DIRECTED)
                or not is_cancel_allowed(declaration.status)
        ):
            raise ContentFailure(
                kinder_conc.CancelResultType.REJECTED, DECL_CANT_REJECTED)

        try:
            declaration.change_status(
                DeclarationStatus.objects.get(code=DSS.REFUSED),
                why_change=WHY_CHANGE,
                date_validation_needed=False,
            )
            cache.set(
                CACHE_REJECTED_WITH_CANCEL_REQUEST.format(declaration.id),
                True, 300
            )
        except DeclarationStatus.DoesNotExist:
            raise ContentFailure(
                kinder_conc.CancelResultType.REJECTED,
                f'Статуса {DSS.values.get(DSS.REFUSED)} не существует')

        response = kinder_conc.FormDataResponseType(
            cancelResponse=kinder_conc.cancelResponseType(
                orderId=int(request.orderId),
                result=kinder_conc.CancelResultType.CANCELLED,
                comment=CANCEL_SUCCESS_COMMENT))

        return response
