"""
Type annotations for b2bi service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_b2bi.client import B2BIClient

    session = get_session()
    async with session.create_client("b2bi") as client:
        client: B2BIClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListCapabilitiesPaginator,
    ListPartnershipsPaginator,
    ListProfilesPaginator,
    ListTransformersPaginator,
)
from .type_defs import (
    CreateCapabilityRequestRequestTypeDef,
    CreateCapabilityResponseTypeDef,
    CreatePartnershipRequestRequestTypeDef,
    CreatePartnershipResponseTypeDef,
    CreateProfileRequestRequestTypeDef,
    CreateProfileResponseTypeDef,
    CreateTransformerRequestRequestTypeDef,
    CreateTransformerResponseTypeDef,
    DeleteCapabilityRequestRequestTypeDef,
    DeletePartnershipRequestRequestTypeDef,
    DeleteProfileRequestRequestTypeDef,
    DeleteTransformerRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCapabilityRequestRequestTypeDef,
    GetCapabilityResponseTypeDef,
    GetPartnershipRequestRequestTypeDef,
    GetPartnershipResponseTypeDef,
    GetProfileRequestRequestTypeDef,
    GetProfileResponseTypeDef,
    GetTransformerJobRequestRequestTypeDef,
    GetTransformerJobResponseTypeDef,
    GetTransformerRequestRequestTypeDef,
    GetTransformerResponseTypeDef,
    ListCapabilitiesRequestRequestTypeDef,
    ListCapabilitiesResponseTypeDef,
    ListPartnershipsRequestRequestTypeDef,
    ListPartnershipsResponseTypeDef,
    ListProfilesRequestRequestTypeDef,
    ListProfilesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTransformersRequestRequestTypeDef,
    ListTransformersResponseTypeDef,
    StartTransformerJobRequestRequestTypeDef,
    StartTransformerJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TestMappingRequestRequestTypeDef,
    TestMappingResponseTypeDef,
    TestParsingRequestRequestTypeDef,
    TestParsingResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateCapabilityRequestRequestTypeDef,
    UpdateCapabilityResponseTypeDef,
    UpdatePartnershipRequestRequestTypeDef,
    UpdatePartnershipResponseTypeDef,
    UpdateProfileRequestRequestTypeDef,
    UpdateProfileResponseTypeDef,
    UpdateTransformerRequestRequestTypeDef,
    UpdateTransformerResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("B2BIClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class B2BIClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        B2BIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#close)
        """

    async def create_capability(
        self, **kwargs: Unpack[CreateCapabilityRequestRequestTypeDef]
    ) -> CreateCapabilityResponseTypeDef:
        """
        Instantiates a capability based on the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.create_capability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#create_capability)
        """

    async def create_partnership(
        self, **kwargs: Unpack[CreatePartnershipRequestRequestTypeDef]
    ) -> CreatePartnershipResponseTypeDef:
        """
        Creates a partnership between a customer and a trading partner, based on the
        supplied
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.create_partnership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#create_partnership)
        """

    async def create_profile(
        self, **kwargs: Unpack[CreateProfileRequestRequestTypeDef]
    ) -> CreateProfileResponseTypeDef:
        """
        Creates a customer profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.create_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#create_profile)
        """

    async def create_transformer(
        self, **kwargs: Unpack[CreateTransformerRequestRequestTypeDef]
    ) -> CreateTransformerResponseTypeDef:
        """
        Creates a transformer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.create_transformer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#create_transformer)
        """

    async def delete_capability(
        self, **kwargs: Unpack[DeleteCapabilityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified capability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.delete_capability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#delete_capability)
        """

    async def delete_partnership(
        self, **kwargs: Unpack[DeletePartnershipRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified partnership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.delete_partnership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#delete_partnership)
        """

    async def delete_profile(
        self, **kwargs: Unpack[DeleteProfileRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.delete_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#delete_profile)
        """

    async def delete_transformer(
        self, **kwargs: Unpack[DeleteTransformerRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified transformer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.delete_transformer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#delete_transformer)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#generate_presigned_url)
        """

    async def get_capability(
        self, **kwargs: Unpack[GetCapabilityRequestRequestTypeDef]
    ) -> GetCapabilityResponseTypeDef:
        """
        Retrieves the details for the specified capability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_capability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_capability)
        """

    async def get_partnership(
        self, **kwargs: Unpack[GetPartnershipRequestRequestTypeDef]
    ) -> GetPartnershipResponseTypeDef:
        """
        Retrieves the details for a partnership, based on the partner and profile IDs
        specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_partnership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_partnership)
        """

    async def get_profile(
        self, **kwargs: Unpack[GetProfileRequestRequestTypeDef]
    ) -> GetProfileResponseTypeDef:
        """
        Retrieves the details for the profile specified by the profile ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_profile)
        """

    async def get_transformer(
        self, **kwargs: Unpack[GetTransformerRequestRequestTypeDef]
    ) -> GetTransformerResponseTypeDef:
        """
        Retrieves the details for the transformer specified by the transformer ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_transformer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_transformer)
        """

    async def get_transformer_job(
        self, **kwargs: Unpack[GetTransformerJobRequestRequestTypeDef]
    ) -> GetTransformerJobResponseTypeDef:
        """
        Returns the details of the transformer run, based on the Transformer job ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_transformer_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_transformer_job)
        """

    async def list_capabilities(
        self, **kwargs: Unpack[ListCapabilitiesRequestRequestTypeDef]
    ) -> ListCapabilitiesResponseTypeDef:
        """
        Lists the capabilities associated with your Amazon Web Services account for
        your current or specified
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.list_capabilities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#list_capabilities)
        """

    async def list_partnerships(
        self, **kwargs: Unpack[ListPartnershipsRequestRequestTypeDef]
    ) -> ListPartnershipsResponseTypeDef:
        """
        Lists the partnerships associated with your Amazon Web Services account for
        your current or specified
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.list_partnerships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#list_partnerships)
        """

    async def list_profiles(
        self, **kwargs: Unpack[ListProfilesRequestRequestTypeDef]
    ) -> ListProfilesResponseTypeDef:
        """
        Lists the profiles associated with your Amazon Web Services account for your
        current or specified
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.list_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#list_profiles)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags associated with the Amazon Resource Name (ARN) that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#list_tags_for_resource)
        """

    async def list_transformers(
        self, **kwargs: Unpack[ListTransformersRequestRequestTypeDef]
    ) -> ListTransformersResponseTypeDef:
        """
        Lists the available transformers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.list_transformers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#list_transformers)
        """

    async def start_transformer_job(
        self, **kwargs: Unpack[StartTransformerJobRequestRequestTypeDef]
    ) -> StartTransformerJobResponseTypeDef:
        """
        Runs a job, using a transformer, to parse input EDI (electronic data
        interchange) file into the output structures used by Amazon Web Services B2BI
        Data
        Interchange.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.start_transformer_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#start_transformer_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a key-value pair to a resource, as identified by its Amazon Resource
        Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#tag_resource)
        """

    async def test_mapping(
        self, **kwargs: Unpack[TestMappingRequestRequestTypeDef]
    ) -> TestMappingResponseTypeDef:
        """
        Maps the input file according to the provided template file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.test_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#test_mapping)
        """

    async def test_parsing(
        self, **kwargs: Unpack[TestParsingRequestRequestTypeDef]
    ) -> TestParsingResponseTypeDef:
        """
        Parses the input EDI (electronic data interchange) file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.test_parsing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#test_parsing)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a key-value pair from the specified resource, as identified by its
        Amazon Resource Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#untag_resource)
        """

    async def update_capability(
        self, **kwargs: Unpack[UpdateCapabilityRequestRequestTypeDef]
    ) -> UpdateCapabilityResponseTypeDef:
        """
        Updates some of the parameters for a capability, based on the specified
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.update_capability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#update_capability)
        """

    async def update_partnership(
        self, **kwargs: Unpack[UpdatePartnershipRequestRequestTypeDef]
    ) -> UpdatePartnershipResponseTypeDef:
        """
        Updates some of the parameters for a partnership between a customer and trading
        partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.update_partnership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#update_partnership)
        """

    async def update_profile(
        self, **kwargs: Unpack[UpdateProfileRequestRequestTypeDef]
    ) -> UpdateProfileResponseTypeDef:
        """
        Updates the specified parameters for a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.update_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#update_profile)
        """

    async def update_transformer(
        self, **kwargs: Unpack[UpdateTransformerRequestRequestTypeDef]
    ) -> UpdateTransformerResponseTypeDef:
        """
        Updates the specified parameters for a transformer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.update_transformer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#update_transformer)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_capabilities"]
    ) -> ListCapabilitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_partnerships"]
    ) -> ListPartnershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_profiles"]) -> ListProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_transformers"]
    ) -> ListTransformersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/#get_paginator)
        """

    async def __aenter__(self) -> "B2BIClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi.html#B2BI.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/client/)
        """
