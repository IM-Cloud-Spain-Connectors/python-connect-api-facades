#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from rndi.connect.business_objects.adapters import Asset, Request
from rndi.connect.api_facades.contracts import OnError, OnSuccess


class AssetManagementService(ABC):
    @abstractmethod
    def find_asset(self, asset_id: str) -> Asset:
        """
        Returns the required Asset Business Object by id.

        :param asset_id: str The unique Asset id: AS-XXXX-XXXX-XXXX
        :return: Asset The required Asset.
        """

    @abstractmethod
    def find_asset_request(self, request_id: str) -> Request:
        """
        Returns the required Asset Request Business Object by id.

        :param request_id: str The unique Request id: PR-XXXX-XXXX-XXXX-NNN
        :return: Request The required Request
        """

    @abstractmethod
    def approve_asset_request(
            self,
            request: Union[dict, Request],
            template_id: str,
            activation_tile: Optional[str] = None,
            effective_date: Optional[str] = None,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Approves the given request using the given template id.

        :param request: The Request object.
        :param template_id: The template id to be used to approve.
        :param activation_tile: The activation tile.
        :param effective_date: The effective date.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: The approved Request.
        """

    @abstractmethod
    def fail_asset_request(
            self,
            request: Union[dict, Request],
            reason: str,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Fail the given request using the given reason.

        :param request: The Request object.
        :param reason: The reason to fail the request.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: The failed Request.
        """

    @abstractmethod
    def inquire_asset_request(
            self,
            request: Union[dict, Request],
            template_id: str,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Inquire the given Request

        :param request: The Request object.
        :param template_id: The template id to be used to inquire.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: The inquired Request.
        """

    @abstractmethod
    def update_asset_request_parameters(
            self,
            request: Union[dict, Request],
            parameters: List[Dict[str, Any]],
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Update Asset parameters

        :param request: The Request object.
        :param parameters: The parameters to update in for the Asset.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: The request
        """

    @abstractmethod
    def _update_asset_request_status(
            self,
            request: Request,
            status: str,
            payload: Dict[str, Any] = None,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Update Asset Request Status

        :param request: The Request object.
        :param status: The template id to be used to inquire.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: Request
        """
