#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from rndi.connect.api_facades.contracts import OnError, OnSuccess
from rndi.connect.business_objects.adapters import Request, TierConfiguration


class TierConfigurationManagementService(ABC):
    @abstractmethod
    def find_tier_configuration(self, tier_configuration_id: str) -> TierConfiguration:
        """
        Returns the required TierConfiguration Business Object by id.

        :param tier_configuration_id: str The unique Tier Configuration id: TC-XXXX-XXXX-XXXX
        :return: TierConfiguration The required TierConfiguration.
        """

    @abstractmethod
    def find_tier_configuration_request(self, request_id: str) -> Request:
        """
        Returns the required TierConfiguration Request Business Object by id.

        :param request_id: str The unique Request id: TCR-XXXX-XXXX-XXXX-NNN
        :return: Request The required Request
        """

    @abstractmethod
    def approve_tier_configuration_request(
            self,
            request: Union[dict, Request],
            template_id: str,
            effective_date: Optional[str] = None,
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Approves the given request using the given template id.

        :param request: The Request object.
        :param template_id: The template id to be used to approve.
        :param effective_date: The effective date.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: The approved Request.
        """

    @abstractmethod
    def fail_tier_configuration_request(
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
    def update_tier_configuration_request_parameters(
            self,
            request: Union[dict, Request],
            parameters: List[Dict[str, Any]],
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Updates the given request parameters.

        :param request: The Request object.
        :param parameters: The parameters to update.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: The updated Request.
        """
        pass

    @abstractmethod
    def inquire_tier_configuration_request(
            self,
            request: Union[dict, Request],
            on_error: Optional[OnError] = None,
            on_success: Optional[OnSuccess] = None,
    ) -> Union[Any, Request]:
        """
        Inquires the given request.

        :param request: The Request object.
        :param on_error: Callback to execute when we got an error.
        :param on_success: Callback to execute when action finished successfully.
        :return: The updated Request.
        """
        pass
