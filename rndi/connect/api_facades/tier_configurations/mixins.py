#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

from connect.client import AsyncConnectClient, ClientError, ConnectClient
from rndi.connect.business_objects.adapters import Request, TierConfiguration
from rndi.connect.api_facades.contracts import OnError, OnSuccess
from rndi.connect.api_facades.tier_configurations.contracts import (
    TierConfigurationManagementService,
)

ID = 'id'
TIER = 'tier'
APPROVE = 'approve'
TEMPLATE = 'template'
FAIL = 'fail'
INQUIRE = 'inquire'


class WithTierConfigurationFacade(TierConfigurationManagementService):
    client: Union[ConnectClient, AsyncConnectClient]

    def find_tier_configuration(self, tier_id: str) -> TierConfiguration:
        return TierConfiguration(self.client.tiers[tier_id].get())

    def find_tier_configuration_request(
            self,
            request_id: str,
    ) -> Request:
        return Request(self.client.requests[request_id].get())

    def update_tier_configuration_request_parameters(
            self,
            request: Union[dict, Request],
            parameters: List[Dict[str, Any]],
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        if on_success is None:
            def on_success(req: Request):
                return req

        if on_error is None:
            def on_error(error: ClientError):
                raise error

        try:
            return on_success(
                request.with_tier_configuration(
                    Request(
                        self.client.ns(TIER).config_requests[request.id()].update({
                            "params": parameters,
                        }),
                    ).tier_configuration(),
                ),
            )
        except ClientError as e:
            return on_error(e)

    def approve_tier_configuration_request(
            self,
            request: Union[dict, Request],
            template_id: str,
            effective_date: Optional[str] = None,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        template = {
            ID: template_id,
            "effective_date": effective_date,
        }
        payload = {TEMPLATE: {k: v for k, v in template.items() if v is not None}}

        return self._update_request_status(request, APPROVE, payload, on_error, on_success)

    def fail_tier_configuration_request(
            self,
            request: Union[dict, Request],
            reason: str,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        payload = {'reason': reason}

        if on_success is None:
            def on_success(req: Request):
                return req.with_reason(reason)

        return self._update_request_status(request, FAIL, payload, on_error, on_success)

    def _update_request_status(
            self,
            request: Request,
            status: str,
            payload: Dict[str, Any] = None,
            on_error: Optional[Callable[[ClientError], Any]] = None,
            on_success: Optional[Callable[[Request], Any]] = None,
    ) -> Union[Any, Request]:
        if on_success is None:
            def on_success(req: Request):
                return req

        if on_error is None:
            def on_error(error: ClientError):
                raise error
        statuses = {
            "approve": "approved",
            "inquire": "inquiring",
            "fail": "failed",
        }
        try:
            self.client.ns(TIER).config_requests[request.id()](status).post(
                payload=payload,
            )
            return on_success(
                request.with_status(statuses.get(status)),
            )
        except ClientError as e:
            return on_error(e)

    def inquire_tier_configuration_request(
            self,
            request: Union[dict, Request],
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        return self._update_request_status(
            request,
            INQUIRE,
            on_error=on_error,
            on_success=on_success,
        )
