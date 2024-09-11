"""
Type annotations for supplychain service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/type_defs/)

Usage::

    ```python
    from types_aiobotocore_supplychain.type_defs import BillOfMaterialsImportJobTypeDef

    data: BillOfMaterialsImportJobTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, Union

from .literals import ConfigurationJobStatusType, DataIntegrationEventTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BillOfMaterialsImportJobTypeDef",
    "CreateBillOfMaterialsImportJobRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetBillOfMaterialsImportJobRequestRequestTypeDef",
    "TimestampTypeDef",
    "CreateBillOfMaterialsImportJobResponseTypeDef",
    "GetBillOfMaterialsImportJobResponseTypeDef",
    "SendDataIntegrationEventResponseTypeDef",
    "SendDataIntegrationEventRequestRequestTypeDef",
)

BillOfMaterialsImportJobTypeDef = TypedDict(
    "BillOfMaterialsImportJobTypeDef",
    {
        "instanceId": str,
        "jobId": str,
        "status": ConfigurationJobStatusType,
        "s3uri": str,
        "message": NotRequired[str],
    },
)
CreateBillOfMaterialsImportJobRequestRequestTypeDef = TypedDict(
    "CreateBillOfMaterialsImportJobRequestRequestTypeDef",
    {
        "instanceId": str,
        "s3uri": str,
        "clientToken": NotRequired[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
GetBillOfMaterialsImportJobRequestRequestTypeDef = TypedDict(
    "GetBillOfMaterialsImportJobRequestRequestTypeDef",
    {
        "instanceId": str,
        "jobId": str,
    },
)
TimestampTypeDef = Union[datetime, str]
CreateBillOfMaterialsImportJobResponseTypeDef = TypedDict(
    "CreateBillOfMaterialsImportJobResponseTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetBillOfMaterialsImportJobResponseTypeDef = TypedDict(
    "GetBillOfMaterialsImportJobResponseTypeDef",
    {
        "job": BillOfMaterialsImportJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SendDataIntegrationEventResponseTypeDef = TypedDict(
    "SendDataIntegrationEventResponseTypeDef",
    {
        "eventId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SendDataIntegrationEventRequestRequestTypeDef = TypedDict(
    "SendDataIntegrationEventRequestRequestTypeDef",
    {
        "instanceId": str,
        "eventType": DataIntegrationEventTypeType,
        "data": str,
        "eventGroupId": str,
        "eventTimestamp": NotRequired[TimestampTypeDef],
        "clientToken": NotRequired[str],
    },
)
