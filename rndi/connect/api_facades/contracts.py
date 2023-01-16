#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import Any, Callable

from connect.client import ClientError
from rndi.connect.business_objects.adapters import Request

OnError = Callable[[ClientError], Any]
OnSuccess = Callable[[Request], Any]
