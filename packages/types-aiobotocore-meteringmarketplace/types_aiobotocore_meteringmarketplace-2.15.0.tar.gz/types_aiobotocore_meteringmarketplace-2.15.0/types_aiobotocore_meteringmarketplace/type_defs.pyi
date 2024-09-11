"""
Type annotations for meteringmarketplace service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_meteringmarketplace/type_defs/)

Usage::

    ```python
    from types_aiobotocore_meteringmarketplace.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import UsageRecordResultStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ResponseMetadataTypeDef",
    "TimestampTypeDef",
    "RegisterUsageRequestRequestTypeDef",
    "ResolveCustomerRequestRequestTypeDef",
    "TagTypeDef",
    "MeterUsageResultTypeDef",
    "RegisterUsageResultTypeDef",
    "ResolveCustomerResultTypeDef",
    "UsageAllocationOutputTypeDef",
    "UsageAllocationTypeDef",
    "UsageRecordOutputTypeDef",
    "UsageAllocationUnionTypeDef",
    "UsageRecordTypeDef",
    "UsageRecordResultTypeDef",
    "MeterUsageRequestRequestTypeDef",
    "UsageRecordUnionTypeDef",
    "BatchMeterUsageResultTypeDef",
    "BatchMeterUsageRequestRequestTypeDef",
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
TimestampTypeDef = Union[datetime, str]
RegisterUsageRequestRequestTypeDef = TypedDict(
    "RegisterUsageRequestRequestTypeDef",
    {
        "ProductCode": str,
        "PublicKeyVersion": int,
        "Nonce": NotRequired[str],
    },
)
ResolveCustomerRequestRequestTypeDef = TypedDict(
    "ResolveCustomerRequestRequestTypeDef",
    {
        "RegistrationToken": str,
    },
)
TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)
MeterUsageResultTypeDef = TypedDict(
    "MeterUsageResultTypeDef",
    {
        "MeteringRecordId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RegisterUsageResultTypeDef = TypedDict(
    "RegisterUsageResultTypeDef",
    {
        "PublicKeyRotationTimestamp": datetime,
        "Signature": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResolveCustomerResultTypeDef = TypedDict(
    "ResolveCustomerResultTypeDef",
    {
        "CustomerIdentifier": str,
        "ProductCode": str,
        "CustomerAWSAccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UsageAllocationOutputTypeDef = TypedDict(
    "UsageAllocationOutputTypeDef",
    {
        "AllocatedUsageQuantity": int,
        "Tags": NotRequired[List[TagTypeDef]],
    },
)
UsageAllocationTypeDef = TypedDict(
    "UsageAllocationTypeDef",
    {
        "AllocatedUsageQuantity": int,
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
UsageRecordOutputTypeDef = TypedDict(
    "UsageRecordOutputTypeDef",
    {
        "Timestamp": datetime,
        "CustomerIdentifier": str,
        "Dimension": str,
        "Quantity": NotRequired[int],
        "UsageAllocations": NotRequired[List[UsageAllocationOutputTypeDef]],
    },
)
UsageAllocationUnionTypeDef = Union[UsageAllocationTypeDef, UsageAllocationOutputTypeDef]
UsageRecordTypeDef = TypedDict(
    "UsageRecordTypeDef",
    {
        "Timestamp": TimestampTypeDef,
        "CustomerIdentifier": str,
        "Dimension": str,
        "Quantity": NotRequired[int],
        "UsageAllocations": NotRequired[Sequence[UsageAllocationTypeDef]],
    },
)
UsageRecordResultTypeDef = TypedDict(
    "UsageRecordResultTypeDef",
    {
        "UsageRecord": NotRequired[UsageRecordOutputTypeDef],
        "MeteringRecordId": NotRequired[str],
        "Status": NotRequired[UsageRecordResultStatusType],
    },
)
MeterUsageRequestRequestTypeDef = TypedDict(
    "MeterUsageRequestRequestTypeDef",
    {
        "ProductCode": str,
        "Timestamp": TimestampTypeDef,
        "UsageDimension": str,
        "UsageQuantity": NotRequired[int],
        "DryRun": NotRequired[bool],
        "UsageAllocations": NotRequired[Sequence[UsageAllocationUnionTypeDef]],
    },
)
UsageRecordUnionTypeDef = Union[UsageRecordTypeDef, UsageRecordOutputTypeDef]
BatchMeterUsageResultTypeDef = TypedDict(
    "BatchMeterUsageResultTypeDef",
    {
        "Results": List[UsageRecordResultTypeDef],
        "UnprocessedRecords": List[UsageRecordOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchMeterUsageRequestRequestTypeDef = TypedDict(
    "BatchMeterUsageRequestRequestTypeDef",
    {
        "UsageRecords": Sequence[UsageRecordUnionTypeDef],
        "ProductCode": str,
    },
)
