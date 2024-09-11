"""
Type annotations for backup-gateway service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_backup_gateway.client import BackupGatewayClient

    session = get_session()
    async with session.create_client("backup-gateway") as client:
        client: BackupGatewayClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListGatewaysPaginator, ListHypervisorsPaginator, ListVirtualMachinesPaginator
from .type_defs import (
    AssociateGatewayToServerInputRequestTypeDef,
    AssociateGatewayToServerOutputTypeDef,
    CreateGatewayInputRequestTypeDef,
    CreateGatewayOutputTypeDef,
    DeleteGatewayInputRequestTypeDef,
    DeleteGatewayOutputTypeDef,
    DeleteHypervisorInputRequestTypeDef,
    DeleteHypervisorOutputTypeDef,
    DisassociateGatewayFromServerInputRequestTypeDef,
    DisassociateGatewayFromServerOutputTypeDef,
    GetBandwidthRateLimitScheduleInputRequestTypeDef,
    GetBandwidthRateLimitScheduleOutputTypeDef,
    GetGatewayInputRequestTypeDef,
    GetGatewayOutputTypeDef,
    GetHypervisorInputRequestTypeDef,
    GetHypervisorOutputTypeDef,
    GetHypervisorPropertyMappingsInputRequestTypeDef,
    GetHypervisorPropertyMappingsOutputTypeDef,
    GetVirtualMachineInputRequestTypeDef,
    GetVirtualMachineOutputTypeDef,
    ImportHypervisorConfigurationInputRequestTypeDef,
    ImportHypervisorConfigurationOutputTypeDef,
    ListGatewaysInputRequestTypeDef,
    ListGatewaysOutputTypeDef,
    ListHypervisorsInputRequestTypeDef,
    ListHypervisorsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualMachinesInputRequestTypeDef,
    ListVirtualMachinesOutputTypeDef,
    PutBandwidthRateLimitScheduleInputRequestTypeDef,
    PutBandwidthRateLimitScheduleOutputTypeDef,
    PutHypervisorPropertyMappingsInputRequestTypeDef,
    PutHypervisorPropertyMappingsOutputTypeDef,
    PutMaintenanceStartTimeInputRequestTypeDef,
    PutMaintenanceStartTimeOutputTypeDef,
    StartVirtualMachinesMetadataSyncInputRequestTypeDef,
    StartVirtualMachinesMetadataSyncOutputTypeDef,
    TagResourceInputRequestTypeDef,
    TagResourceOutputTypeDef,
    TestHypervisorConfigurationInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UntagResourceOutputTypeDef,
    UpdateGatewayInformationInputRequestTypeDef,
    UpdateGatewayInformationOutputTypeDef,
    UpdateGatewaySoftwareNowInputRequestTypeDef,
    UpdateGatewaySoftwareNowOutputTypeDef,
    UpdateHypervisorInputRequestTypeDef,
    UpdateHypervisorOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("BackupGatewayClient",)

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
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class BackupGatewayClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BackupGatewayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#exceptions)
        """

    async def associate_gateway_to_server(
        self, **kwargs: Unpack[AssociateGatewayToServerInputRequestTypeDef]
    ) -> AssociateGatewayToServerOutputTypeDef:
        """
        Associates a backup gateway with your server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.associate_gateway_to_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#associate_gateway_to_server)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#close)
        """

    async def create_gateway(
        self, **kwargs: Unpack[CreateGatewayInputRequestTypeDef]
    ) -> CreateGatewayOutputTypeDef:
        """
        Creates a backup gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.create_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#create_gateway)
        """

    async def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayInputRequestTypeDef]
    ) -> DeleteGatewayOutputTypeDef:
        """
        Deletes a backup gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.delete_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#delete_gateway)
        """

    async def delete_hypervisor(
        self, **kwargs: Unpack[DeleteHypervisorInputRequestTypeDef]
    ) -> DeleteHypervisorOutputTypeDef:
        """
        Deletes a hypervisor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.delete_hypervisor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#delete_hypervisor)
        """

    async def disassociate_gateway_from_server(
        self, **kwargs: Unpack[DisassociateGatewayFromServerInputRequestTypeDef]
    ) -> DisassociateGatewayFromServerOutputTypeDef:
        """
        Disassociates a backup gateway from the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.disassociate_gateway_from_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#disassociate_gateway_from_server)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#generate_presigned_url)
        """

    async def get_bandwidth_rate_limit_schedule(
        self, **kwargs: Unpack[GetBandwidthRateLimitScheduleInputRequestTypeDef]
    ) -> GetBandwidthRateLimitScheduleOutputTypeDef:
        """
        Retrieves the bandwidth rate limit schedule for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_bandwidth_rate_limit_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_bandwidth_rate_limit_schedule)
        """

    async def get_gateway(
        self, **kwargs: Unpack[GetGatewayInputRequestTypeDef]
    ) -> GetGatewayOutputTypeDef:
        """
        By providing the ARN (Amazon Resource Name), this API returns the gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_gateway)
        """

    async def get_hypervisor(
        self, **kwargs: Unpack[GetHypervisorInputRequestTypeDef]
    ) -> GetHypervisorOutputTypeDef:
        """
        This action requests information about the specified hypervisor to which the
        gateway will
        connect.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_hypervisor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_hypervisor)
        """

    async def get_hypervisor_property_mappings(
        self, **kwargs: Unpack[GetHypervisorPropertyMappingsInputRequestTypeDef]
    ) -> GetHypervisorPropertyMappingsOutputTypeDef:
        """
        This action retrieves the property mappings for the specified hypervisor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_hypervisor_property_mappings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_hypervisor_property_mappings)
        """

    async def get_virtual_machine(
        self, **kwargs: Unpack[GetVirtualMachineInputRequestTypeDef]
    ) -> GetVirtualMachineOutputTypeDef:
        """
        By providing the ARN (Amazon Resource Name), this API returns the virtual
        machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_virtual_machine)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_virtual_machine)
        """

    async def import_hypervisor_configuration(
        self, **kwargs: Unpack[ImportHypervisorConfigurationInputRequestTypeDef]
    ) -> ImportHypervisorConfigurationOutputTypeDef:
        """
        Connect to a hypervisor by importing its configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.import_hypervisor_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#import_hypervisor_configuration)
        """

    async def list_gateways(
        self, **kwargs: Unpack[ListGatewaysInputRequestTypeDef]
    ) -> ListGatewaysOutputTypeDef:
        """
        Lists backup gateways owned by an Amazon Web Services account in an Amazon Web
        Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_gateways)
        """

    async def list_hypervisors(
        self, **kwargs: Unpack[ListHypervisorsInputRequestTypeDef]
    ) -> ListHypervisorsOutputTypeDef:
        """
        Lists your hypervisors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_hypervisors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_hypervisors)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags applied to the resource identified by its Amazon Resource Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_tags_for_resource)
        """

    async def list_virtual_machines(
        self, **kwargs: Unpack[ListVirtualMachinesInputRequestTypeDef]
    ) -> ListVirtualMachinesOutputTypeDef:
        """
        Lists your virtual machines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_virtual_machines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_virtual_machines)
        """

    async def put_bandwidth_rate_limit_schedule(
        self, **kwargs: Unpack[PutBandwidthRateLimitScheduleInputRequestTypeDef]
    ) -> PutBandwidthRateLimitScheduleOutputTypeDef:
        """
        This action sets the bandwidth rate limit schedule for a specified gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.put_bandwidth_rate_limit_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#put_bandwidth_rate_limit_schedule)
        """

    async def put_hypervisor_property_mappings(
        self, **kwargs: Unpack[PutHypervisorPropertyMappingsInputRequestTypeDef]
    ) -> PutHypervisorPropertyMappingsOutputTypeDef:
        """
        This action sets the property mappings for the specified hypervisor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.put_hypervisor_property_mappings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#put_hypervisor_property_mappings)
        """

    async def put_maintenance_start_time(
        self, **kwargs: Unpack[PutMaintenanceStartTimeInputRequestTypeDef]
    ) -> PutMaintenanceStartTimeOutputTypeDef:
        """
        Set the maintenance start time for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.put_maintenance_start_time)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#put_maintenance_start_time)
        """

    async def start_virtual_machines_metadata_sync(
        self, **kwargs: Unpack[StartVirtualMachinesMetadataSyncInputRequestTypeDef]
    ) -> StartVirtualMachinesMetadataSyncOutputTypeDef:
        """
        This action sends a request to sync metadata across the specified virtual
        machines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.start_virtual_machines_metadata_sync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#start_virtual_machines_metadata_sync)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> TagResourceOutputTypeDef:
        """
        Tag the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#tag_resource)
        """

    async def test_hypervisor_configuration(
        self, **kwargs: Unpack[TestHypervisorConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Tests your hypervisor configuration to validate that backup gateway can connect
        with the hypervisor and its
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.test_hypervisor_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#test_hypervisor_configuration)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> UntagResourceOutputTypeDef:
        """
        Removes tags from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#untag_resource)
        """

    async def update_gateway_information(
        self, **kwargs: Unpack[UpdateGatewayInformationInputRequestTypeDef]
    ) -> UpdateGatewayInformationOutputTypeDef:
        """
        Updates a gateway's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.update_gateway_information)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#update_gateway_information)
        """

    async def update_gateway_software_now(
        self, **kwargs: Unpack[UpdateGatewaySoftwareNowInputRequestTypeDef]
    ) -> UpdateGatewaySoftwareNowOutputTypeDef:
        """
        Updates the gateway virtual machine (VM) software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.update_gateway_software_now)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#update_gateway_software_now)
        """

    async def update_hypervisor(
        self, **kwargs: Unpack[UpdateHypervisorInputRequestTypeDef]
    ) -> UpdateHypervisorOutputTypeDef:
        """
        Updates a hypervisor metadata, including its host, username, and password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.update_hypervisor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#update_hypervisor)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hypervisors"]
    ) -> ListHypervisorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_machines"]
    ) -> ListVirtualMachinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_paginator)
        """

    async def __aenter__(self) -> "BackupGatewayClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)
        """
