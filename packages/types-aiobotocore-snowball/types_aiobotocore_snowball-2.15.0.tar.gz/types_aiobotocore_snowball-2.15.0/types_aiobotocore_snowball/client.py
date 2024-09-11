"""
Type annotations for snowball service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_snowball.client import SnowballClient

    session = get_session()
    async with session.create_client("snowball") as client:
        client: SnowballClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeAddressesPaginator,
    ListClusterJobsPaginator,
    ListClustersPaginator,
    ListCompatibleImagesPaginator,
    ListJobsPaginator,
    ListLongTermPricingPaginator,
)
from .type_defs import (
    CancelClusterRequestRequestTypeDef,
    CancelJobRequestRequestTypeDef,
    CreateAddressRequestRequestTypeDef,
    CreateAddressResultTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResultTypeDef,
    CreateJobRequestRequestTypeDef,
    CreateJobResultTypeDef,
    CreateLongTermPricingRequestRequestTypeDef,
    CreateLongTermPricingResultTypeDef,
    CreateReturnShippingLabelRequestRequestTypeDef,
    CreateReturnShippingLabelResultTypeDef,
    DescribeAddressesRequestRequestTypeDef,
    DescribeAddressesResultTypeDef,
    DescribeAddressRequestRequestTypeDef,
    DescribeAddressResultTypeDef,
    DescribeClusterRequestRequestTypeDef,
    DescribeClusterResultTypeDef,
    DescribeJobRequestRequestTypeDef,
    DescribeJobResultTypeDef,
    DescribeReturnShippingLabelRequestRequestTypeDef,
    DescribeReturnShippingLabelResultTypeDef,
    GetJobManifestRequestRequestTypeDef,
    GetJobManifestResultTypeDef,
    GetJobUnlockCodeRequestRequestTypeDef,
    GetJobUnlockCodeResultTypeDef,
    GetSnowballUsageResultTypeDef,
    GetSoftwareUpdatesRequestRequestTypeDef,
    GetSoftwareUpdatesResultTypeDef,
    ListClusterJobsRequestRequestTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesRequestRequestTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResultTypeDef,
    ListLongTermPricingRequestRequestTypeDef,
    ListLongTermPricingResultTypeDef,
    ListPickupLocationsRequestRequestTypeDef,
    ListPickupLocationsResultTypeDef,
    ListServiceVersionsRequestRequestTypeDef,
    ListServiceVersionsResultTypeDef,
    UpdateClusterRequestRequestTypeDef,
    UpdateJobRequestRequestTypeDef,
    UpdateJobShipmentStateRequestRequestTypeDef,
    UpdateLongTermPricingRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SnowballClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClusterLimitExceededException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    Ec2RequestFailedException: Type[BotocoreClientError]
    InvalidAddressException: Type[BotocoreClientError]
    InvalidInputCombinationException: Type[BotocoreClientError]
    InvalidJobStateException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidResourceException: Type[BotocoreClientError]
    KMSRequestFailedException: Type[BotocoreClientError]
    ReturnShippingLabelAlreadyExistsException: Type[BotocoreClientError]
    UnsupportedAddressException: Type[BotocoreClientError]


class SnowballClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SnowballClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#can_paginate)
        """

    async def cancel_cluster(
        self, **kwargs: Unpack[CancelClusterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a cluster job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.cancel_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#cancel_cluster)
        """

    async def cancel_job(self, **kwargs: Unpack[CancelJobRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Cancels the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.cancel_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#cancel_job)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#close)
        """

    async def create_address(
        self, **kwargs: Unpack[CreateAddressRequestRequestTypeDef]
    ) -> CreateAddressResultTypeDef:
        """
        Creates an address for a Snow device to be shipped to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.create_address)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_address)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResultTypeDef:
        """
        Creates an empty cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.create_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_cluster)
        """

    async def create_job(
        self, **kwargs: Unpack[CreateJobRequestRequestTypeDef]
    ) -> CreateJobResultTypeDef:
        """
        Creates a job to import or export data between Amazon S3 and your on-premises
        data
        center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_job)
        """

    async def create_long_term_pricing(
        self, **kwargs: Unpack[CreateLongTermPricingRequestRequestTypeDef]
    ) -> CreateLongTermPricingResultTypeDef:
        """
        Creates a job with the long-term usage option for a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.create_long_term_pricing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_long_term_pricing)
        """

    async def create_return_shipping_label(
        self, **kwargs: Unpack[CreateReturnShippingLabelRequestRequestTypeDef]
    ) -> CreateReturnShippingLabelResultTypeDef:
        """
        Creates a shipping label that will be used to return the Snow device to Amazon
        Web
        Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.create_return_shipping_label)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#create_return_shipping_label)
        """

    async def describe_address(
        self, **kwargs: Unpack[DescribeAddressRequestRequestTypeDef]
    ) -> DescribeAddressResultTypeDef:
        """
        Takes an `AddressId` and returns specific details about that address in the
        form of an `Address`
        object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.describe_address)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_address)
        """

    async def describe_addresses(
        self, **kwargs: Unpack[DescribeAddressesRequestRequestTypeDef]
    ) -> DescribeAddressesResultTypeDef:
        """
        Returns a specified number of `ADDRESS` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.describe_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_addresses)
        """

    async def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestRequestTypeDef]
    ) -> DescribeClusterResultTypeDef:
        """
        Returns information about a specific cluster including shipping information,
        cluster status, and other important
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.describe_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_cluster)
        """

    async def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestRequestTypeDef]
    ) -> DescribeJobResultTypeDef:
        """
        Returns information about a specific job including shipping information, job
        status, and other important
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.describe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_job)
        """

    async def describe_return_shipping_label(
        self, **kwargs: Unpack[DescribeReturnShippingLabelRequestRequestTypeDef]
    ) -> DescribeReturnShippingLabelResultTypeDef:
        """
        Information on the shipping label of a Snow device that is being returned to
        Amazon Web
        Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.describe_return_shipping_label)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#describe_return_shipping_label)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#generate_presigned_url)
        """

    async def get_job_manifest(
        self, **kwargs: Unpack[GetJobManifestRequestRequestTypeDef]
    ) -> GetJobManifestResultTypeDef:
        """
        Returns a link to an Amazon S3 presigned URL for the manifest file associated
        with the specified `JobId`
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_job_manifest)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_job_manifest)
        """

    async def get_job_unlock_code(
        self, **kwargs: Unpack[GetJobUnlockCodeRequestRequestTypeDef]
    ) -> GetJobUnlockCodeResultTypeDef:
        """
        Returns the `UnlockCode` code value for the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_job_unlock_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_job_unlock_code)
        """

    async def get_snowball_usage(self) -> GetSnowballUsageResultTypeDef:
        """
        Returns information about the Snow Family service limit for your account, and
        also the number of Snow devices your account has in
        use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_snowball_usage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_snowball_usage)
        """

    async def get_software_updates(
        self, **kwargs: Unpack[GetSoftwareUpdatesRequestRequestTypeDef]
    ) -> GetSoftwareUpdatesResultTypeDef:
        """
        Returns an Amazon S3 presigned URL for an update file associated with a
        specified
        `JobId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_software_updates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_software_updates)
        """

    async def list_cluster_jobs(
        self, **kwargs: Unpack[ListClusterJobsRequestRequestTypeDef]
    ) -> ListClusterJobsResultTypeDef:
        """
        Returns an array of `JobListEntry` objects of the specified length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.list_cluster_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_cluster_jobs)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResultTypeDef:
        """
        Returns an array of `ClusterListEntry` objects of the specified length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.list_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_clusters)
        """

    async def list_compatible_images(
        self, **kwargs: Unpack[ListCompatibleImagesRequestRequestTypeDef]
    ) -> ListCompatibleImagesResultTypeDef:
        """
        This action returns a list of the different Amazon EC2-compatible Amazon
        Machine Images (AMIs) that are owned by your Amazon Web Services accountthat
        would be supported for use on a Snow
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.list_compatible_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_compatible_images)
        """

    async def list_jobs(
        self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]
    ) -> ListJobsResultTypeDef:
        """
        Returns an array of `JobListEntry` objects of the specified length.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_jobs)
        """

    async def list_long_term_pricing(
        self, **kwargs: Unpack[ListLongTermPricingRequestRequestTypeDef]
    ) -> ListLongTermPricingResultTypeDef:
        """
        Lists all long-term pricing types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.list_long_term_pricing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_long_term_pricing)
        """

    async def list_pickup_locations(
        self, **kwargs: Unpack[ListPickupLocationsRequestRequestTypeDef]
    ) -> ListPickupLocationsResultTypeDef:
        """
        A list of locations from which the customer can choose to pickup a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.list_pickup_locations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_pickup_locations)
        """

    async def list_service_versions(
        self, **kwargs: Unpack[ListServiceVersionsRequestRequestTypeDef]
    ) -> ListServiceVersionsResultTypeDef:
        """
        Lists all supported versions for Snow on-device services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.list_service_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#list_service_versions)
        """

    async def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        While a cluster's `ClusterState` value is in the `AwaitingQuorum` state, you
        can update some of the information associated with a
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.update_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_cluster)
        """

    async def update_job(self, **kwargs: Unpack[UpdateJobRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        While a job's `JobState` value is `New`, you can update some of the information
        associated with a
        job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.update_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_job)
        """

    async def update_job_shipment_state(
        self, **kwargs: Unpack[UpdateJobShipmentStateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the state when a shipment state changes to a different state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.update_job_shipment_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_job_shipment_state)
        """

    async def update_long_term_pricing(
        self, **kwargs: Unpack[UpdateLongTermPricingRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the long-term pricing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.update_long_term_pricing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#update_long_term_pricing)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_addresses"]
    ) -> DescribeAddressesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cluster_jobs"]
    ) -> ListClusterJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compatible_images"]
    ) -> ListCompatibleImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_long_term_pricing"]
    ) -> ListLongTermPricingPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/#get_paginator)
        """

    async def __aenter__(self) -> "SnowballClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/client/)
        """
