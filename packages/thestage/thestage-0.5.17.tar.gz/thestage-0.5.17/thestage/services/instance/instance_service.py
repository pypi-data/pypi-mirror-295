from typing import List, Optional, Dict

import typer
from thestage_core.entities.config_entity import ConfigEntity

from thestage.i18n.translation import __
from thestage.services.clients.thestage_api.dtos.enums.selfhosted_status import SelfhostedBusinessStatus
from thestage.services.clients.thestage_api.dtos.enums.instance_rented_status import InstanceRentedBusinessStatus
from thestage.services.abstract_service import AbstractService
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.clients.thestage_api.dtos.instance_rented_response import InstanceRentedDto
from thestage.services.clients.thestage_api.dtos.paginated_entity_list import PaginatedEntityList
from thestage.services.clients.thestage_api.dtos.selfhosted_instance_response import SelfHostedInstanceDto
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.remote_server_service import RemoteServerService


class InstanceService(AbstractService):

    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
            remote_server_service: RemoteServerService,
    ):
        super(InstanceService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client
        self.__remote_server_service = remote_server_service

    def get_rented_item(
            self,
            config: ConfigEntity,
            instance_slug: str,
    ) -> Optional[InstanceRentedDto]:
        return self.__thestage_api_client.get_rented_item(
            token=config.main.thestage_auth_token,
            instance_slug=instance_slug,
        )

    def get_self_hosted_item(
            self,
            config: ConfigEntity,
            instance_slug: str,
    ) -> Optional[SelfHostedInstanceDto]:
        return self.__thestage_api_client.get_selfhosted_item(
            token=config.main.thestage_auth_token,
            instance_slug=instance_slug,
        )

    @error_handler()
    def check_instance_status_to_connect(
            self,
            instance: InstanceRentedDto,
    ) -> InstanceRentedDto:
        if instance:
            if instance.frontend_status.status_key in [
                InstanceRentedBusinessStatus.IN_QUEUE.name,
                InstanceRentedBusinessStatus.CREATING.name,
                InstanceRentedBusinessStatus.REBOOTING.name,
                InstanceRentedBusinessStatus.STARTING.name,
            ]:
                typer.echo(__('Cannot connect to rented server instance: it is either in the process of being rented or rebooted'))
                raise typer.Exit(1)
            elif instance.frontend_status.status_key in [
                InstanceRentedBusinessStatus.TERMINATING.name,
                InstanceRentedBusinessStatus.RENTAL_ERROR.name,
            ]:
                typer.echo(__('Cannot connect to rented server instance: renting process failed'))
                raise typer.Exit(1)
            elif instance.frontend_status.status_key in [
                InstanceRentedBusinessStatus.STOPPED.name,
                InstanceRentedBusinessStatus.STOPPING.name,
                InstanceRentedBusinessStatus.DELETED.name,
            ]:
                typer.echo(__('Cannot connect to rented server instance: it is either stopped or has been deleted'))
                raise typer.Exit(1)
            elif instance.frontend_status.status_key in [
                InstanceRentedBusinessStatus.UNKNOWN.name,
                InstanceRentedBusinessStatus.ALL.name,
            ]:
                typer.echo(__('Cannot connect to rented server instance: instance status unknown'))
                raise typer.Exit(1)

        return instance

    @error_handler()
    def check_selfhosted_status_to_connect(
            self,
            instance: SelfHostedInstanceDto,
    ) -> SelfHostedInstanceDto:
        if instance:
            if instance.frontend_status.status_key in [
                SelfhostedBusinessStatus.AWAITING_CONFIGURATION.name,
            ]:
                typer.echo(__('Cannot connect to self-hosted instance: it is awaiting configuration'))
                raise typer.Exit(1)
            elif instance.frontend_status.status_key in [
                SelfhostedBusinessStatus.TERMINATED.name,
                SelfhostedBusinessStatus.DELETED.name,
            ]:
                typer.echo(__('Cannot connect to self-hosted instance: it may be turned off or unreachable'))
                raise typer.Exit(1)
            elif instance.frontend_status.status_key in [
                SelfhostedBusinessStatus.UNKNOWN.name,
                SelfhostedBusinessStatus.ALL.name,
            ]:
                typer.echo(__('Cannot connect to self-hosted instance: instance status unknown'))
                raise typer.Exit(1)

        return instance

    @error_handler()
    def connect_to_rented_instance(
            self,
            instance_rented_slug: str,
            config: ConfigEntity,
    ):
        instance = self.get_rented_item(config=config, instance_slug=instance_rented_slug)

        if instance:
            self.check_instance_status_to_connect(
                instance=instance,
            )
            self.__remote_server_service.connect_to_instance(
                ip_address=instance.ip_address,
                username=instance.host_username,
            )
        else:
            typer.echo(__("Server instance not found: %instance_item%", {'instance_item': instance_rented_slug}))


    @error_handler()
    def connect_to_selfhosted_instance(
            self,
            selfhosted_instance_slug: str,
            username: str,
            config: ConfigEntity,
    ):
        instance = self.get_self_hosted_item(config=config, instance_slug=selfhosted_instance_slug)

        if instance:
            self.check_selfhosted_status_to_connect(
                instance=instance,
            )
            self.__remote_server_service.connect_to_instance(
                ip_address=instance.ip_address,
                username=username or instance.host_username or 'root',
            )
        else:
            typer.echo(__("Server instance not found: %instance_item%", {'instance_item': selfhosted_instance_slug}))


    @error_handler()
    def get_rented_list(
            self,
            config: ConfigEntity,
            statuses: List[str],
            row: int = 5,
            page: int = 1,
    ) -> PaginatedEntityList[InstanceRentedDto]:
        data = self.__thestage_api_client.get_rented_instance_list(
            token=config.main.thestage_auth_token,
            statuses=statuses,
            page=page,
            limit=row,
        )

        return data

    @error_handler()
    def get_self_hosted_list(
            self,
            config: ConfigEntity,
            statuses: List[str],
            row: int = 5,
            page: int = 1,
    ) -> PaginatedEntityList[SelfHostedInstanceDto]:
        data = self.__thestage_api_client.get_selfhosted_instance_list(
            token=config.main.thestage_auth_token,
            statuses=statuses,
            page=page,
            limit=row,
        )
        return data
