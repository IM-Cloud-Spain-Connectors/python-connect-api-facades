#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from connect.client import AsyncConnectClient, ClientError, ConnectClient
from rndi.connect.business_objects.adapters import Asset, Request
from rndi.connect.api_facades.assets.contracts import AssetManagementService
from rndi.connect.api_facades.contracts import OnError, OnSuccess

APPROVE = 'approve'
INQUIRE = 'inquire'
FAIL = 'fail'
APPROVED = 'approved'
INQUIRING = 'inquiring'
FAILED = 'failed'
TEMPLATE_ID = 'template_id'
ACTIVATION_TILE = 'activation_tile'
EFFECTIVE_DATE = 'effective_date'
REASON = 'reason'


class WithAssetFacade(AssetManagementService):
    client: Union[ConnectClient, AsyncConnectClient]

    def find_asset(self, asset_id: str) -> Asset:
        return Asset(self.client.assets[asset_id].get())

    def find_asset_request(self, request_id: str) -> Request:
        return Request(self.client.requests[request_id].get())

    def approve_asset_request(
            self,
            request: Union[dict, Request],
            template_id: str,
            activation_tile: Optional[str] = None,
            effective_date: Optional[str] = None,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:

        request = request if isinstance(request, Request) else Request(request)

        payload = {
            TEMPLATE_ID: template_id,
            ACTIVATION_TILE: activation_tile,
            EFFECTIVE_DATE: effective_date,
        }

        return self._update_asset_request_status(
            request,
            APPROVE,
            payload,
            on_error,
            on_success,
        )

    def fail_asset_request(
            self,
            request: Union[dict, Request],
            reason: str,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        request = request if isinstance(request, Request) else Request(request)

        payload = {REASON: reason}
        request.with_reason(reason)

        return self._update_asset_request_status(
            request,
            FAIL,
            payload,
            on_error,
            on_success,
        )

    def inquire_asset_request(
            self,
            request: Union[dict, Request],
            template_id: str,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        request = request if isinstance(request, Request) else Request(request)

        payload = {
            TEMPLATE_ID: template_id,
        }

        return self._update_asset_request_status(
            request,
            INQUIRE,
            payload,
            on_error,
            on_success,
        )

    def update_asset_request_parameters(
            self,
            request: Union[dict, Request],
            parameters: List[Dict[str, Any]],
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        request = request if isinstance(request, Request) else Request(request)

        if on_success is None:
            def on_success(request_: Request) -> Request:
                return request_

        if on_error is None:
            def on_error(error: ClientError):
                raise error
        try:
            updated = Request(self.client.requests[request.id()].update(payload={
                "asset": {
                    "params": parameters,
                },
            }))

            return on_success(request.with_asset(updated.asset()))
        except ClientError as e:
            return on_error(e)

    def _update_asset_request_status(
            self,
            request: Request,
            status: str,
            payload: Dict[str, Any] = None,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        if on_success is None:
            def on_success(req: Request):
                return req

        if on_error is None:
            def on_error(error: ClientError):
                raise error

        statuses = {
            APPROVE: APPROVED,
            INQUIRE: INQUIRING,
            FAIL: FAILED,
        }

        try:
            self.client.requests[request.id()](status).post(
                # cleanup the none values of the payload.
                payload={k: v for k, v in payload.items() if v is not None},
            )
            return on_success(request.with_status(statuses.get(status)))
        except ClientError as e:
            return on_error(e)
