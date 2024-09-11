"""
Type annotations for managedblockchain service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_managedblockchain.client import ManagedBlockchainClient

    session = get_session()
    async with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListAccessorsPaginator
from .type_defs import (
    CreateAccessorInputRequestTypeDef,
    CreateAccessorOutputTypeDef,
    CreateMemberInputRequestTypeDef,
    CreateMemberOutputTypeDef,
    CreateNetworkInputRequestTypeDef,
    CreateNetworkOutputTypeDef,
    CreateNodeInputRequestTypeDef,
    CreateNodeOutputTypeDef,
    CreateProposalInputRequestTypeDef,
    CreateProposalOutputTypeDef,
    DeleteAccessorInputRequestTypeDef,
    DeleteMemberInputRequestTypeDef,
    DeleteNodeInputRequestTypeDef,
    GetAccessorInputRequestTypeDef,
    GetAccessorOutputTypeDef,
    GetMemberInputRequestTypeDef,
    GetMemberOutputTypeDef,
    GetNetworkInputRequestTypeDef,
    GetNetworkOutputTypeDef,
    GetNodeInputRequestTypeDef,
    GetNodeOutputTypeDef,
    GetProposalInputRequestTypeDef,
    GetProposalOutputTypeDef,
    ListAccessorsInputRequestTypeDef,
    ListAccessorsOutputTypeDef,
    ListInvitationsInputRequestTypeDef,
    ListInvitationsOutputTypeDef,
    ListMembersInputRequestTypeDef,
    ListMembersOutputTypeDef,
    ListNetworksInputRequestTypeDef,
    ListNetworksOutputTypeDef,
    ListNodesInputRequestTypeDef,
    ListNodesOutputTypeDef,
    ListProposalsInputRequestTypeDef,
    ListProposalsOutputTypeDef,
    ListProposalVotesInputRequestTypeDef,
    ListProposalVotesOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RejectInvitationInputRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateMemberInputRequestTypeDef,
    UpdateNodeInputRequestTypeDef,
    VoteOnProposalInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ManagedBlockchainClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IllegalActionException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class ManagedBlockchainClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedBlockchainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#close)
        """

    async def create_accessor(
        self, **kwargs: Unpack[CreateAccessorInputRequestTypeDef]
    ) -> CreateAccessorOutputTypeDef:
        """
        Creates a new accessor for use with Amazon Managed Blockchain service that
        supports token based
        access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_accessor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_accessor)
        """

    async def create_member(
        self, **kwargs: Unpack[CreateMemberInputRequestTypeDef]
    ) -> CreateMemberOutputTypeDef:
        """
        Creates a member within a Managed Blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_member)
        """

    async def create_network(
        self, **kwargs: Unpack[CreateNetworkInputRequestTypeDef]
    ) -> CreateNetworkOutputTypeDef:
        """
        Creates a new blockchain network using Amazon Managed Blockchain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_network)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_network)
        """

    async def create_node(
        self, **kwargs: Unpack[CreateNodeInputRequestTypeDef]
    ) -> CreateNodeOutputTypeDef:
        """
        Creates a node on the specified blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_node)
        """

    async def create_proposal(
        self, **kwargs: Unpack[CreateProposalInputRequestTypeDef]
    ) -> CreateProposalOutputTypeDef:
        """
        Creates a proposal for a change to the network that other members of the
        network can vote on, for example, a proposal to add a new member to the
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.create_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_proposal)
        """

    async def delete_accessor(
        self, **kwargs: Unpack[DeleteAccessorInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an accessor that your Amazon Web Services account owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.delete_accessor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_accessor)
        """

    async def delete_member(
        self, **kwargs: Unpack[DeleteMemberInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.delete_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_member)
        """

    async def delete_node(self, **kwargs: Unpack[DeleteNodeInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a node that your Amazon Web Services account owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.delete_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_node)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#generate_presigned_url)
        """

    async def get_accessor(
        self, **kwargs: Unpack[GetAccessorInputRequestTypeDef]
    ) -> GetAccessorOutputTypeDef:
        """
        Returns detailed information about an accessor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_accessor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_accessor)
        """

    async def get_member(
        self, **kwargs: Unpack[GetMemberInputRequestTypeDef]
    ) -> GetMemberOutputTypeDef:
        """
        Returns detailed information about a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_member)
        """

    async def get_network(
        self, **kwargs: Unpack[GetNetworkInputRequestTypeDef]
    ) -> GetNetworkOutputTypeDef:
        """
        Returns detailed information about a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_network)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_network)
        """

    async def get_node(self, **kwargs: Unpack[GetNodeInputRequestTypeDef]) -> GetNodeOutputTypeDef:
        """
        Returns detailed information about a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_node)
        """

    async def get_proposal(
        self, **kwargs: Unpack[GetProposalInputRequestTypeDef]
    ) -> GetProposalOutputTypeDef:
        """
        Returns detailed information about a proposal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_proposal)
        """

    async def list_accessors(
        self, **kwargs: Unpack[ListAccessorsInputRequestTypeDef]
    ) -> ListAccessorsOutputTypeDef:
        """
        Returns a list of the accessors and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_accessors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_accessors)
        """

    async def list_invitations(
        self, **kwargs: Unpack[ListInvitationsInputRequestTypeDef]
    ) -> ListInvitationsOutputTypeDef:
        """
        Returns a list of all invitations for the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_invitations)
        """

    async def list_members(
        self, **kwargs: Unpack[ListMembersInputRequestTypeDef]
    ) -> ListMembersOutputTypeDef:
        """
        Returns a list of the members in a network and properties of their
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_members)
        """

    async def list_networks(
        self, **kwargs: Unpack[ListNetworksInputRequestTypeDef]
    ) -> ListNetworksOutputTypeDef:
        """
        Returns information about the networks in which the current Amazon Web Services
        account
        participates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_networks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_networks)
        """

    async def list_nodes(
        self, **kwargs: Unpack[ListNodesInputRequestTypeDef]
    ) -> ListNodesOutputTypeDef:
        """
        Returns information about the nodes within a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_nodes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_nodes)
        """

    async def list_proposal_votes(
        self, **kwargs: Unpack[ListProposalVotesInputRequestTypeDef]
    ) -> ListProposalVotesOutputTypeDef:
        """
        Returns the list of votes for a specified proposal, including the value of each
        vote and the unique identifier of the member that cast the
        vote.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_proposal_votes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_proposal_votes)
        """

    async def list_proposals(
        self, **kwargs: Unpack[ListProposalsInputRequestTypeDef]
    ) -> ListProposalsOutputTypeDef:
        """
        Returns a list of proposals for the network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_proposals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_proposals)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_tags_for_resource)
        """

    async def reject_invitation(
        self, **kwargs: Unpack[RejectInvitationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Rejects an invitation to join a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.reject_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#reject_invitation)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or overwrites the specified tags for the specified Amazon Managed
        Blockchain
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the Amazon Managed Blockchain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#untag_resource)
        """

    async def update_member(
        self, **kwargs: Unpack[UpdateMemberInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a member configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.update_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#update_member)
        """

    async def update_node(self, **kwargs: Unpack[UpdateNodeInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a node configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.update_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#update_node)
        """

    async def vote_on_proposal(
        self, **kwargs: Unpack[VoteOnProposalInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Casts a vote for a specified `ProposalId` on behalf of a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.vote_on_proposal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#vote_on_proposal)
        """

    def get_paginator(self, operation_name: Literal["list_accessors"]) -> ListAccessorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_paginator)
        """

    async def __aenter__(self) -> "ManagedBlockchainClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
        """
