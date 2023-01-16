#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import Union

from connect.client import AsyncConnectClient, ConnectClient
from rndi.connect.api_facades.assets.mixins import WithAssetFacade


class ConnectOpenAPIFacade(
    WithAssetFacade,
):
    def __init__(self, client: Union[ConnectClient, AsyncConnectClient]):
        self._client = client

    @property
    def client(self) -> ConnectClient:
        return self._client
