"""
Type annotations for s3 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3.client import S3Client

    session = get_session()
    async with session.create_client("s3") as client:
        client: S3Client
    ```
"""

import sys
from typing import Any, Callable, Dict, List, Mapping, Optional, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListBucketsPaginator,
    ListDirectoryBucketsPaginator,
    ListMultipartUploadsPaginator,
    ListObjectsPaginator,
    ListObjectsV2Paginator,
    ListObjectVersionsPaginator,
    ListPartsPaginator,
)
from .type_defs import (
    AbortMultipartUploadOutputTypeDef,
    AbortMultipartUploadRequestRequestTypeDef,
    CompleteMultipartUploadOutputTypeDef,
    CompleteMultipartUploadRequestRequestTypeDef,
    CopyObjectOutputTypeDef,
    CopyObjectRequestRequestTypeDef,
    CopySourceTypeDef,
    CreateBucketOutputTypeDef,
    CreateBucketRequestRequestTypeDef,
    CreateMultipartUploadOutputTypeDef,
    CreateMultipartUploadRequestRequestTypeDef,
    CreateSessionOutputTypeDef,
    CreateSessionRequestRequestTypeDef,
    DeleteBucketAnalyticsConfigurationRequestRequestTypeDef,
    DeleteBucketCorsRequestRequestTypeDef,
    DeleteBucketEncryptionRequestRequestTypeDef,
    DeleteBucketIntelligentTieringConfigurationRequestRequestTypeDef,
    DeleteBucketInventoryConfigurationRequestRequestTypeDef,
    DeleteBucketLifecycleRequestRequestTypeDef,
    DeleteBucketMetricsConfigurationRequestRequestTypeDef,
    DeleteBucketOwnershipControlsRequestRequestTypeDef,
    DeleteBucketPolicyRequestRequestTypeDef,
    DeleteBucketReplicationRequestRequestTypeDef,
    DeleteBucketRequestRequestTypeDef,
    DeleteBucketTaggingRequestRequestTypeDef,
    DeleteBucketWebsiteRequestRequestTypeDef,
    DeleteObjectOutputTypeDef,
    DeleteObjectRequestRequestTypeDef,
    DeleteObjectsOutputTypeDef,
    DeleteObjectsRequestRequestTypeDef,
    DeleteObjectTaggingOutputTypeDef,
    DeleteObjectTaggingRequestRequestTypeDef,
    DeletePublicAccessBlockRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    FileobjTypeDef,
    GetBucketAccelerateConfigurationOutputTypeDef,
    GetBucketAccelerateConfigurationRequestRequestTypeDef,
    GetBucketAclOutputTypeDef,
    GetBucketAclRequestRequestTypeDef,
    GetBucketAnalyticsConfigurationOutputTypeDef,
    GetBucketAnalyticsConfigurationRequestRequestTypeDef,
    GetBucketCorsOutputTypeDef,
    GetBucketCorsRequestRequestTypeDef,
    GetBucketEncryptionOutputTypeDef,
    GetBucketEncryptionRequestRequestTypeDef,
    GetBucketIntelligentTieringConfigurationOutputTypeDef,
    GetBucketIntelligentTieringConfigurationRequestRequestTypeDef,
    GetBucketInventoryConfigurationOutputTypeDef,
    GetBucketInventoryConfigurationRequestRequestTypeDef,
    GetBucketLifecycleConfigurationOutputTypeDef,
    GetBucketLifecycleConfigurationRequestRequestTypeDef,
    GetBucketLifecycleOutputTypeDef,
    GetBucketLifecycleRequestRequestTypeDef,
    GetBucketLocationOutputTypeDef,
    GetBucketLocationRequestRequestTypeDef,
    GetBucketLoggingOutputTypeDef,
    GetBucketLoggingRequestRequestTypeDef,
    GetBucketMetricsConfigurationOutputTypeDef,
    GetBucketMetricsConfigurationRequestRequestTypeDef,
    GetBucketNotificationConfigurationRequestRequestTypeDef,
    GetBucketOwnershipControlsOutputTypeDef,
    GetBucketOwnershipControlsRequestRequestTypeDef,
    GetBucketPolicyOutputTypeDef,
    GetBucketPolicyRequestRequestTypeDef,
    GetBucketPolicyStatusOutputTypeDef,
    GetBucketPolicyStatusRequestRequestTypeDef,
    GetBucketReplicationOutputTypeDef,
    GetBucketReplicationRequestRequestTypeDef,
    GetBucketRequestPaymentOutputTypeDef,
    GetBucketRequestPaymentRequestRequestTypeDef,
    GetBucketTaggingOutputTypeDef,
    GetBucketTaggingRequestRequestTypeDef,
    GetBucketVersioningOutputTypeDef,
    GetBucketVersioningRequestRequestTypeDef,
    GetBucketWebsiteOutputTypeDef,
    GetBucketWebsiteRequestRequestTypeDef,
    GetObjectAclOutputTypeDef,
    GetObjectAclRequestRequestTypeDef,
    GetObjectAttributesOutputTypeDef,
    GetObjectAttributesRequestRequestTypeDef,
    GetObjectLegalHoldOutputTypeDef,
    GetObjectLegalHoldRequestRequestTypeDef,
    GetObjectLockConfigurationOutputTypeDef,
    GetObjectLockConfigurationRequestRequestTypeDef,
    GetObjectOutputTypeDef,
    GetObjectRequestRequestTypeDef,
    GetObjectRetentionOutputTypeDef,
    GetObjectRetentionRequestRequestTypeDef,
    GetObjectTaggingOutputTypeDef,
    GetObjectTaggingRequestRequestTypeDef,
    GetObjectTorrentOutputTypeDef,
    GetObjectTorrentRequestRequestTypeDef,
    GetPublicAccessBlockOutputTypeDef,
    GetPublicAccessBlockRequestRequestTypeDef,
    HeadBucketOutputTypeDef,
    HeadBucketRequestRequestTypeDef,
    HeadObjectOutputTypeDef,
    HeadObjectRequestRequestTypeDef,
    ListBucketAnalyticsConfigurationsOutputTypeDef,
    ListBucketAnalyticsConfigurationsRequestRequestTypeDef,
    ListBucketIntelligentTieringConfigurationsOutputTypeDef,
    ListBucketIntelligentTieringConfigurationsRequestRequestTypeDef,
    ListBucketInventoryConfigurationsOutputTypeDef,
    ListBucketInventoryConfigurationsRequestRequestTypeDef,
    ListBucketMetricsConfigurationsOutputTypeDef,
    ListBucketMetricsConfigurationsRequestRequestTypeDef,
    ListBucketsOutputTypeDef,
    ListBucketsRequestRequestTypeDef,
    ListDirectoryBucketsOutputTypeDef,
    ListDirectoryBucketsRequestRequestTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListMultipartUploadsRequestRequestTypeDef,
    ListObjectsOutputTypeDef,
    ListObjectsRequestRequestTypeDef,
    ListObjectsV2OutputTypeDef,
    ListObjectsV2RequestRequestTypeDef,
    ListObjectVersionsOutputTypeDef,
    ListObjectVersionsRequestRequestTypeDef,
    ListPartsOutputTypeDef,
    ListPartsRequestRequestTypeDef,
    NotificationConfigurationDeprecatedResponseTypeDef,
    NotificationConfigurationResponseTypeDef,
    PutBucketAccelerateConfigurationRequestRequestTypeDef,
    PutBucketAclRequestRequestTypeDef,
    PutBucketAnalyticsConfigurationRequestRequestTypeDef,
    PutBucketCorsRequestRequestTypeDef,
    PutBucketEncryptionRequestRequestTypeDef,
    PutBucketIntelligentTieringConfigurationRequestRequestTypeDef,
    PutBucketInventoryConfigurationRequestRequestTypeDef,
    PutBucketLifecycleConfigurationRequestRequestTypeDef,
    PutBucketLifecycleRequestRequestTypeDef,
    PutBucketLoggingRequestRequestTypeDef,
    PutBucketMetricsConfigurationRequestRequestTypeDef,
    PutBucketNotificationConfigurationRequestRequestTypeDef,
    PutBucketNotificationRequestRequestTypeDef,
    PutBucketOwnershipControlsRequestRequestTypeDef,
    PutBucketPolicyRequestRequestTypeDef,
    PutBucketReplicationRequestRequestTypeDef,
    PutBucketRequestPaymentRequestRequestTypeDef,
    PutBucketTaggingRequestRequestTypeDef,
    PutBucketVersioningRequestRequestTypeDef,
    PutBucketWebsiteRequestRequestTypeDef,
    PutObjectAclOutputTypeDef,
    PutObjectAclRequestRequestTypeDef,
    PutObjectLegalHoldOutputTypeDef,
    PutObjectLegalHoldRequestRequestTypeDef,
    PutObjectLockConfigurationOutputTypeDef,
    PutObjectLockConfigurationRequestRequestTypeDef,
    PutObjectOutputTypeDef,
    PutObjectRequestRequestTypeDef,
    PutObjectRetentionOutputTypeDef,
    PutObjectRetentionRequestRequestTypeDef,
    PutObjectTaggingOutputTypeDef,
    PutObjectTaggingRequestRequestTypeDef,
    PutPublicAccessBlockRequestRequestTypeDef,
    RestoreObjectOutputTypeDef,
    RestoreObjectRequestRequestTypeDef,
    SelectObjectContentOutputTypeDef,
    SelectObjectContentRequestRequestTypeDef,
    UploadPartCopyOutputTypeDef,
    UploadPartCopyRequestRequestTypeDef,
    UploadPartOutputTypeDef,
    UploadPartRequestRequestTypeDef,
    WriteGetObjectResponseRequestRequestTypeDef,
)
from .waiter import (
    BucketExistsWaiter,
    BucketNotExistsWaiter,
    ObjectExistsWaiter,
    ObjectNotExistsWaiter,
)

try:
    from boto3.s3.transfer import TransferConfig
except ImportError:
    from builtins import object as TransferConfig
if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("S3Client",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BucketAlreadyExists: Type[BotocoreClientError]
    BucketAlreadyOwnedByYou: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidObjectState: Type[BotocoreClientError]
    NoSuchBucket: Type[BotocoreClientError]
    NoSuchKey: Type[BotocoreClientError]
    NoSuchUpload: Type[BotocoreClientError]
    ObjectAlreadyInActiveTierError: Type[BotocoreClientError]
    ObjectNotInActiveTierError: Type[BotocoreClientError]

class S3Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#exceptions)
        """

    async def abort_multipart_upload(
        self, **kwargs: Unpack[AbortMultipartUploadRequestRequestTypeDef]
    ) -> AbortMultipartUploadOutputTypeDef:
        """
        This operation aborts a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.abort_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#abort_multipart_upload)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#close)
        """

    async def complete_multipart_upload(
        self, **kwargs: Unpack[CompleteMultipartUploadRequestRequestTypeDef]
    ) -> CompleteMultipartUploadOutputTypeDef:
        """
        Completes a multipart upload by assembling previously uploaded parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.complete_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#complete_multipart_upload)
        """

    async def copy(
        self,
        CopySource: CopySourceTypeDef,
        Bucket: str,
        Key: str,
        ExtraArgs: Optional[Dict[str, Any]] = ...,
        Callback: Optional[Callable[..., Any]] = ...,
        SourceClient: Optional[AioBaseClient] = ...,
        Config: Optional[TransferConfig] = ...,
    ) -> None:
        """
        Copy an object from one S3 location to another.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.copy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#copy)
        """

    async def copy_object(
        self, **kwargs: Unpack[CopyObjectRequestRequestTypeDef]
    ) -> CopyObjectOutputTypeDef:
        """
        Creates a copy of an object that is already stored in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.copy_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#copy_object)
        """

    async def create_bucket(
        self, **kwargs: Unpack[CreateBucketRequestRequestTypeDef]
    ) -> CreateBucketOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#create_bucket)
        """

    async def create_multipart_upload(
        self, **kwargs: Unpack[CreateMultipartUploadRequestRequestTypeDef]
    ) -> CreateMultipartUploadOutputTypeDef:
        """
        This action initiates a multipart upload and returns an upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#create_multipart_upload)
        """

    async def create_session(
        self, **kwargs: Unpack[CreateSessionRequestRequestTypeDef]
    ) -> CreateSessionOutputTypeDef:
        """
        Creates a session that establishes temporary security credentials to support
        fast authentication and authorization for the Zonal endpoint APIs on directory
        buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#create_session)
        """

    async def delete_bucket(
        self, **kwargs: Unpack[DeleteBucketRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket)
        """

    async def delete_bucket_analytics_configuration(
        self, **kwargs: Unpack[DeleteBucketAnalyticsConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_analytics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_analytics_configuration)
        """

    async def delete_bucket_cors(
        self, **kwargs: Unpack[DeleteBucketCorsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_cors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_cors)
        """

    async def delete_bucket_encryption(
        self, **kwargs: Unpack[DeleteBucketEncryptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_encryption)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_encryption)
        """

    async def delete_bucket_intelligent_tiering_configuration(
        self, **kwargs: Unpack[DeleteBucketIntelligentTieringConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_intelligent_tiering_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_intelligent_tiering_configuration)
        """

    async def delete_bucket_inventory_configuration(
        self, **kwargs: Unpack[DeleteBucketInventoryConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_inventory_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_inventory_configuration)
        """

    async def delete_bucket_lifecycle(
        self, **kwargs: Unpack[DeleteBucketLifecycleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_lifecycle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_lifecycle)
        """

    async def delete_bucket_metrics_configuration(
        self, **kwargs: Unpack[DeleteBucketMetricsConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_metrics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_metrics_configuration)
        """

    async def delete_bucket_ownership_controls(
        self, **kwargs: Unpack[DeleteBucketOwnershipControlsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_ownership_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_ownership_controls)
        """

    async def delete_bucket_policy(
        self, **kwargs: Unpack[DeleteBucketPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the policy of a specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_policy)
        """

    async def delete_bucket_replication(
        self, **kwargs: Unpack[DeleteBucketReplicationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_replication)
        """

    async def delete_bucket_tagging(
        self, **kwargs: Unpack[DeleteBucketTaggingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_tagging)
        """

    async def delete_bucket_website(
        self, **kwargs: Unpack[DeleteBucketWebsiteRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_website)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_website)
        """

    async def delete_object(
        self, **kwargs: Unpack[DeleteObjectRequestRequestTypeDef]
    ) -> DeleteObjectOutputTypeDef:
        """
        Removes an object from a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_object)
        """

    async def delete_object_tagging(
        self, **kwargs: Unpack[DeleteObjectTaggingRequestRequestTypeDef]
    ) -> DeleteObjectTaggingOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_object_tagging)
        """

    async def delete_objects(
        self, **kwargs: Unpack[DeleteObjectsRequestRequestTypeDef]
    ) -> DeleteObjectsOutputTypeDef:
        """
        This operation enables you to delete multiple objects from a bucket using a
        single HTTP
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_objects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_objects)
        """

    async def delete_public_access_block(
        self, **kwargs: Unpack[DeletePublicAccessBlockRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_public_access_block)
        """

    async def download_file(
        self,
        Bucket: str,
        Key: str,
        Filename: str,
        ExtraArgs: Optional[Dict[str, Any]] = ...,
        Callback: Optional[Callable[..., Any]] = ...,
        Config: Optional[TransferConfig] = ...,
    ) -> None:
        """
        Download an S3 object to a file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#download_file)
        """

    async def download_fileobj(
        self,
        Bucket: str,
        Key: str,
        Fileobj: FileobjTypeDef,
        ExtraArgs: Optional[Dict[str, Any]] = ...,
        Callback: Optional[Callable[..., Any]] = ...,
        Config: Optional[TransferConfig] = ...,
    ) -> None:
        """
        Download an object from S3 to a file-like object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_fileobj)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#download_fileobj)
        """

    async def generate_presigned_post(
        self,
        Bucket: str,
        Key: str,
        Fields: Optional[Dict[str, Any]] = ...,
        Conditions: Union[List[Any], Dict[str, Any], None] = ...,
        ExpiresIn: int = 3600,
    ) -> Dict[str, Any]:
        """
        Builds the url and the form fields used for a presigned s3 post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_post)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#generate_presigned_post)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#generate_presigned_url)
        """

    async def get_bucket_accelerate_configuration(
        self, **kwargs: Unpack[GetBucketAccelerateConfigurationRequestRequestTypeDef]
    ) -> GetBucketAccelerateConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_accelerate_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_accelerate_configuration)
        """

    async def get_bucket_acl(
        self, **kwargs: Unpack[GetBucketAclRequestRequestTypeDef]
    ) -> GetBucketAclOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_acl)
        """

    async def get_bucket_analytics_configuration(
        self, **kwargs: Unpack[GetBucketAnalyticsConfigurationRequestRequestTypeDef]
    ) -> GetBucketAnalyticsConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_analytics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_analytics_configuration)
        """

    async def get_bucket_cors(
        self, **kwargs: Unpack[GetBucketCorsRequestRequestTypeDef]
    ) -> GetBucketCorsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_cors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_cors)
        """

    async def get_bucket_encryption(
        self, **kwargs: Unpack[GetBucketEncryptionRequestRequestTypeDef]
    ) -> GetBucketEncryptionOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_encryption)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_encryption)
        """

    async def get_bucket_intelligent_tiering_configuration(
        self, **kwargs: Unpack[GetBucketIntelligentTieringConfigurationRequestRequestTypeDef]
    ) -> GetBucketIntelligentTieringConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_intelligent_tiering_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_intelligent_tiering_configuration)
        """

    async def get_bucket_inventory_configuration(
        self, **kwargs: Unpack[GetBucketInventoryConfigurationRequestRequestTypeDef]
    ) -> GetBucketInventoryConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_inventory_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_inventory_configuration)
        """

    async def get_bucket_lifecycle(
        self, **kwargs: Unpack[GetBucketLifecycleRequestRequestTypeDef]
    ) -> GetBucketLifecycleOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_lifecycle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_lifecycle)
        """

    async def get_bucket_lifecycle_configuration(
        self, **kwargs: Unpack[GetBucketLifecycleConfigurationRequestRequestTypeDef]
    ) -> GetBucketLifecycleConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_lifecycle_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_lifecycle_configuration)
        """

    async def get_bucket_location(
        self, **kwargs: Unpack[GetBucketLocationRequestRequestTypeDef]
    ) -> GetBucketLocationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_location)
        """

    async def get_bucket_logging(
        self, **kwargs: Unpack[GetBucketLoggingRequestRequestTypeDef]
    ) -> GetBucketLoggingOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_logging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_logging)
        """

    async def get_bucket_metrics_configuration(
        self, **kwargs: Unpack[GetBucketMetricsConfigurationRequestRequestTypeDef]
    ) -> GetBucketMetricsConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_metrics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_metrics_configuration)
        """

    async def get_bucket_notification(
        self, **kwargs: Unpack[GetBucketNotificationConfigurationRequestRequestTypeDef]
    ) -> NotificationConfigurationDeprecatedResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_notification)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_notification)
        """

    async def get_bucket_notification_configuration(
        self, **kwargs: Unpack[GetBucketNotificationConfigurationRequestRequestTypeDef]
    ) -> NotificationConfigurationResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_notification_configuration)
        """

    async def get_bucket_ownership_controls(
        self, **kwargs: Unpack[GetBucketOwnershipControlsRequestRequestTypeDef]
    ) -> GetBucketOwnershipControlsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_ownership_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_ownership_controls)
        """

    async def get_bucket_policy(
        self, **kwargs: Unpack[GetBucketPolicyRequestRequestTypeDef]
    ) -> GetBucketPolicyOutputTypeDef:
        """
        Returns the policy of a specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_policy)
        """

    async def get_bucket_policy_status(
        self, **kwargs: Unpack[GetBucketPolicyStatusRequestRequestTypeDef]
    ) -> GetBucketPolicyStatusOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_policy_status)
        """

    async def get_bucket_replication(
        self, **kwargs: Unpack[GetBucketReplicationRequestRequestTypeDef]
    ) -> GetBucketReplicationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_replication)
        """

    async def get_bucket_request_payment(
        self, **kwargs: Unpack[GetBucketRequestPaymentRequestRequestTypeDef]
    ) -> GetBucketRequestPaymentOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_request_payment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_request_payment)
        """

    async def get_bucket_tagging(
        self, **kwargs: Unpack[GetBucketTaggingRequestRequestTypeDef]
    ) -> GetBucketTaggingOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_tagging)
        """

    async def get_bucket_versioning(
        self, **kwargs: Unpack[GetBucketVersioningRequestRequestTypeDef]
    ) -> GetBucketVersioningOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_versioning)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_versioning)
        """

    async def get_bucket_website(
        self, **kwargs: Unpack[GetBucketWebsiteRequestRequestTypeDef]
    ) -> GetBucketWebsiteOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_website)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_website)
        """

    async def get_object(
        self, **kwargs: Unpack[GetObjectRequestRequestTypeDef]
    ) -> GetObjectOutputTypeDef:
        """
        Retrieves an object from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object)
        """

    async def get_object_acl(
        self, **kwargs: Unpack[GetObjectAclRequestRequestTypeDef]
    ) -> GetObjectAclOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_acl)
        """

    async def get_object_attributes(
        self, **kwargs: Unpack[GetObjectAttributesRequestRequestTypeDef]
    ) -> GetObjectAttributesOutputTypeDef:
        """
        Retrieves all the metadata from an object without returning the object itself.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_attributes)
        """

    async def get_object_legal_hold(
        self, **kwargs: Unpack[GetObjectLegalHoldRequestRequestTypeDef]
    ) -> GetObjectLegalHoldOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_legal_hold)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_legal_hold)
        """

    async def get_object_lock_configuration(
        self, **kwargs: Unpack[GetObjectLockConfigurationRequestRequestTypeDef]
    ) -> GetObjectLockConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_lock_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_lock_configuration)
        """

    async def get_object_retention(
        self, **kwargs: Unpack[GetObjectRetentionRequestRequestTypeDef]
    ) -> GetObjectRetentionOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_retention)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_retention)
        """

    async def get_object_tagging(
        self, **kwargs: Unpack[GetObjectTaggingRequestRequestTypeDef]
    ) -> GetObjectTaggingOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_tagging)
        """

    async def get_object_torrent(
        self, **kwargs: Unpack[GetObjectTorrentRequestRequestTypeDef]
    ) -> GetObjectTorrentOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_torrent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_torrent)
        """

    async def get_public_access_block(
        self, **kwargs: Unpack[GetPublicAccessBlockRequestRequestTypeDef]
    ) -> GetPublicAccessBlockOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_public_access_block)
        """

    async def head_bucket(
        self, **kwargs: Unpack[HeadBucketRequestRequestTypeDef]
    ) -> HeadBucketOutputTypeDef:
        """
        You can use this operation to determine if a bucket exists and if you have
        permission to access
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#head_bucket)
        """

    async def head_object(
        self, **kwargs: Unpack[HeadObjectRequestRequestTypeDef]
    ) -> HeadObjectOutputTypeDef:
        """
        The `HEAD` operation retrieves metadata from an object without returning the
        object
        itself.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#head_object)
        """

    async def list_bucket_analytics_configurations(
        self, **kwargs: Unpack[ListBucketAnalyticsConfigurationsRequestRequestTypeDef]
    ) -> ListBucketAnalyticsConfigurationsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_analytics_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_analytics_configurations)
        """

    async def list_bucket_intelligent_tiering_configurations(
        self, **kwargs: Unpack[ListBucketIntelligentTieringConfigurationsRequestRequestTypeDef]
    ) -> ListBucketIntelligentTieringConfigurationsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_intelligent_tiering_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_intelligent_tiering_configurations)
        """

    async def list_bucket_inventory_configurations(
        self, **kwargs: Unpack[ListBucketInventoryConfigurationsRequestRequestTypeDef]
    ) -> ListBucketInventoryConfigurationsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_inventory_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_inventory_configurations)
        """

    async def list_bucket_metrics_configurations(
        self, **kwargs: Unpack[ListBucketMetricsConfigurationsRequestRequestTypeDef]
    ) -> ListBucketMetricsConfigurationsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_metrics_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_metrics_configurations)
        """

    async def list_buckets(
        self, **kwargs: Unpack[ListBucketsRequestRequestTypeDef]
    ) -> ListBucketsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_buckets)
        """

    async def list_directory_buckets(
        self, **kwargs: Unpack[ListDirectoryBucketsRequestRequestTypeDef]
    ) -> ListDirectoryBucketsOutputTypeDef:
        """
        Returns a list of all Amazon S3 directory buckets owned by the authenticated
        sender of the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_directory_buckets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_directory_buckets)
        """

    async def list_multipart_uploads(
        self, **kwargs: Unpack[ListMultipartUploadsRequestRequestTypeDef]
    ) -> ListMultipartUploadsOutputTypeDef:
        """
        This operation lists in-progress multipart uploads in a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_multipart_uploads)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_multipart_uploads)
        """

    async def list_object_versions(
        self, **kwargs: Unpack[ListObjectVersionsRequestRequestTypeDef]
    ) -> ListObjectVersionsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_object_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_object_versions)
        """

    async def list_objects(
        self, **kwargs: Unpack[ListObjectsRequestRequestTypeDef]
    ) -> ListObjectsOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_objects)
        """

    async def list_objects_v2(
        self, **kwargs: Unpack[ListObjectsV2RequestRequestTypeDef]
    ) -> ListObjectsV2OutputTypeDef:
        """
        Returns some or all (up to 1,000) of the objects in a bucket with each request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_objects_v2)
        """

    async def list_parts(
        self, **kwargs: Unpack[ListPartsRequestRequestTypeDef]
    ) -> ListPartsOutputTypeDef:
        """
        Lists the parts that have been uploaded for a specific multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_parts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_parts)
        """

    async def put_bucket_accelerate_configuration(
        self, **kwargs: Unpack[PutBucketAccelerateConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_accelerate_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_accelerate_configuration)
        """

    async def put_bucket_acl(
        self, **kwargs: Unpack[PutBucketAclRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_acl)
        """

    async def put_bucket_analytics_configuration(
        self, **kwargs: Unpack[PutBucketAnalyticsConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_analytics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_analytics_configuration)
        """

    async def put_bucket_cors(
        self, **kwargs: Unpack[PutBucketCorsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_cors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_cors)
        """

    async def put_bucket_encryption(
        self, **kwargs: Unpack[PutBucketEncryptionRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_encryption)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_encryption)
        """

    async def put_bucket_intelligent_tiering_configuration(
        self, **kwargs: Unpack[PutBucketIntelligentTieringConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_intelligent_tiering_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_intelligent_tiering_configuration)
        """

    async def put_bucket_inventory_configuration(
        self, **kwargs: Unpack[PutBucketInventoryConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_inventory_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_inventory_configuration)
        """

    async def put_bucket_lifecycle(
        self, **kwargs: Unpack[PutBucketLifecycleRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_lifecycle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_lifecycle)
        """

    async def put_bucket_lifecycle_configuration(
        self, **kwargs: Unpack[PutBucketLifecycleConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_lifecycle_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_lifecycle_configuration)
        """

    async def put_bucket_logging(
        self, **kwargs: Unpack[PutBucketLoggingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_logging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_logging)
        """

    async def put_bucket_metrics_configuration(
        self, **kwargs: Unpack[PutBucketMetricsConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_metrics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_metrics_configuration)
        """

    async def put_bucket_notification(
        self, **kwargs: Unpack[PutBucketNotificationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_notification)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_notification)
        """

    async def put_bucket_notification_configuration(
        self, **kwargs: Unpack[PutBucketNotificationConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_notification_configuration)
        """

    async def put_bucket_ownership_controls(
        self, **kwargs: Unpack[PutBucketOwnershipControlsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_ownership_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_ownership_controls)
        """

    async def put_bucket_policy(
        self, **kwargs: Unpack[PutBucketPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Applies an Amazon S3 bucket policy to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_policy)
        """

    async def put_bucket_replication(
        self, **kwargs: Unpack[PutBucketReplicationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_replication)
        """

    async def put_bucket_request_payment(
        self, **kwargs: Unpack[PutBucketRequestPaymentRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_request_payment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_request_payment)
        """

    async def put_bucket_tagging(
        self, **kwargs: Unpack[PutBucketTaggingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_tagging)
        """

    async def put_bucket_versioning(
        self, **kwargs: Unpack[PutBucketVersioningRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_versioning)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_versioning)
        """

    async def put_bucket_website(
        self, **kwargs: Unpack[PutBucketWebsiteRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_website)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_website)
        """

    async def put_object(
        self, **kwargs: Unpack[PutObjectRequestRequestTypeDef]
    ) -> PutObjectOutputTypeDef:
        """
        Adds an object to a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object)
        """

    async def put_object_acl(
        self, **kwargs: Unpack[PutObjectAclRequestRequestTypeDef]
    ) -> PutObjectAclOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_acl)
        """

    async def put_object_legal_hold(
        self, **kwargs: Unpack[PutObjectLegalHoldRequestRequestTypeDef]
    ) -> PutObjectLegalHoldOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_legal_hold)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_legal_hold)
        """

    async def put_object_lock_configuration(
        self, **kwargs: Unpack[PutObjectLockConfigurationRequestRequestTypeDef]
    ) -> PutObjectLockConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_lock_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_lock_configuration)
        """

    async def put_object_retention(
        self, **kwargs: Unpack[PutObjectRetentionRequestRequestTypeDef]
    ) -> PutObjectRetentionOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_retention)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_retention)
        """

    async def put_object_tagging(
        self, **kwargs: Unpack[PutObjectTaggingRequestRequestTypeDef]
    ) -> PutObjectTaggingOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_tagging)
        """

    async def put_public_access_block(
        self, **kwargs: Unpack[PutPublicAccessBlockRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_public_access_block)
        """

    async def restore_object(
        self, **kwargs: Unpack[RestoreObjectRequestRequestTypeDef]
    ) -> RestoreObjectOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.restore_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#restore_object)
        """

    async def select_object_content(
        self, **kwargs: Unpack[SelectObjectContentRequestRequestTypeDef]
    ) -> SelectObjectContentOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.select_object_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#select_object_content)
        """

    async def upload_file(
        self,
        Filename: str,
        Bucket: str,
        Key: str,
        ExtraArgs: Optional[Dict[str, Any]] = ...,
        Callback: Optional[Callable[..., Any]] = ...,
        Config: Optional[TransferConfig] = ...,
    ) -> None:
        """
        Upload a file to an S3 object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_file)
        """

    async def upload_fileobj(
        self,
        Fileobj: FileobjTypeDef,
        Bucket: str,
        Key: str,
        ExtraArgs: Optional[Dict[str, Any]] = ...,
        Callback: Optional[Callable[..., Any]] = ...,
        Config: Optional[TransferConfig] = ...,
    ) -> None:
        """
        Upload a file-like object to S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_fileobj)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_fileobj)
        """

    async def upload_part(
        self, **kwargs: Unpack[UploadPartRequestRequestTypeDef]
    ) -> UploadPartOutputTypeDef:
        """
        Uploads a part in a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_part)
        """

    async def upload_part_copy(
        self, **kwargs: Unpack[UploadPartCopyRequestRequestTypeDef]
    ) -> UploadPartCopyOutputTypeDef:
        """
        Uploads a part by copying data from an existing object as data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_part_copy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_part_copy)
        """

    async def write_get_object_response(
        self, **kwargs: Unpack[WriteGetObjectResponseRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.write_get_object_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#write_get_object_response)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_buckets"]) -> ListBucketsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_directory_buckets"]
    ) -> ListDirectoryBucketsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multipart_uploads"]
    ) -> ListMultipartUploadsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_object_versions"]
    ) -> ListObjectVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_objects"]) -> ListObjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_objects_v2"]) -> ListObjectsV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_parts"]) -> ListPartsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["bucket_exists"]) -> BucketExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["bucket_not_exists"]) -> BucketNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["object_exists"]) -> ObjectExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["object_not_exists"]) -> ObjectNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """

    async def __aenter__(self) -> "S3Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)
        """
