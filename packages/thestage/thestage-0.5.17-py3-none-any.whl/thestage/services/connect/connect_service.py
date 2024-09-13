from typing import List, Optional, Dict

import typer
from thestage_core.entities.config_entity import ConfigEntity
from thestage_core.exceptions.http_error_exception import HttpClientException

from thestage.helpers.logger.app_logger import app_logger
from thestage.i18n.translation import __
from thestage.services.clients.thestage_api.dtos.enums.container_status import DockerContainerStatus
from thestage.services.clients.thestage_api.dtos.enums.selfhosted_status import SelfhostedBusinessStatus
from thestage.services.clients.thestage_api.dtos.enums.instance_rented_status import InstanceRentedBusinessStatus
from thestage.services.abstract_service import AbstractService
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.clients.thestage_api.dtos.instance_rented_response import InstanceRentedDto
from thestage.services.clients.thestage_api.dtos.paginated_entity_list import PaginatedEntityList
from thestage.services.clients.thestage_api.dtos.selfhosted_instance_response import SelfHostedInstanceDto
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.container.container_service import ContainerService
from thestage.services.instance.instance_service import InstanceService
from thestage.services.remote_server_service import RemoteServerService


class ConnectService(AbstractService):
    __thestage_api_client: TheStageApiClient = None
    __instance_service: InstanceService = None
    __container_service: ContainerService = None

    def __init__(
            self,
            config_provider: ConfigProvider,
            thestage_api_client: TheStageApiClient,
            instance_service: InstanceService,
            container_service: ContainerService,
    ):
        super(ConnectService, self).__init__(
            config_provider=config_provider,
        )
        self.__thestage_api_client = thestage_api_client
        self.__instance_service = instance_service
        self.__container_service = container_service


    @error_handler()
    def connect_to_entity(
            self,
            uid: str,
            username: Optional[str]
    ):
        config = self._config_provider.get_full_config()

        try:
            instance_selfhosted = self.__thestage_api_client.get_selfhosted_item(token=config.main.thestage_auth_token, instance_slug=uid)
        except HttpClientException as e:
            instance_selfhosted = None

        try:
            instance_rented = self.__thestage_api_client.get_rented_item(token=config.main.thestage_auth_token, instance_slug=uid)
        except HttpClientException as e:
            instance_rented = None

        try:
            container = self.__thestage_api_client.get_container(token=config.main.thestage_auth_token, container_slug=uid, )
        except Exception as e:
            container = None

        rented_exists = int(instance_rented is not None and instance_rented.frontend_status.status_key == InstanceRentedBusinessStatus.ONLINE)
        selfhosted_exists = int(instance_selfhosted is not None)
        container_exists = int(container is not None)

        rented_presence = int(rented_exists and instance_rented.frontend_status.status_key == InstanceRentedBusinessStatus.ONLINE)
        selfhosted_presence = int(selfhosted_exists and instance_selfhosted.frontend_status.status_key == SelfhostedBusinessStatus.RUNNING)
        container_presence = int(container_exists and container.frontend_status.status_key == DockerContainerStatus.RUNNING)

        if (rented_presence + selfhosted_presence + container_presence) == 0:
            typer.echo(__("There is nothing to connect to with the provided UID"))
            raise typer.Exit(code=1)

        if rented_exists:
            typer.echo(__("Found a rented instance with the provided UID in status: %rented_status%", {"rented_status": instance_rented.frontend_status.status_translation}))

        if selfhosted_exists:
            typer.echo(__("Found a self-hosted instance with the provided UID in status: %selfhosted_status%", {"selfhosted_status": instance_selfhosted.frontend_status.status_translation}))

        if container_exists:
            typer.echo(__("Found a docker container with the provided UID in status: %container_status%", {"container_status": container.frontend_status.status_translation}))

        if (rented_presence + selfhosted_presence + container_presence) > 1:
            typer.echo(__("Provided UID caused ambiguity"))
            typer.echo(__("Consider running a dedicated command to connect to the entity you need"))
            raise typer.Exit(code=1)

        if rented_presence:
            typer.echo(__("Connecting to rented instance..."))
            self.__instance_service.connect_to_rented_instance(
                instance_rented_slug=uid,
                config=config
            )

        if container_presence:
            typer.echo(__("Connecting to docker container..."))
            self.__container_service.check_container_status_for_work(
                container=container
            )
            self.__container_service.connect_container(
                config=config,
                container=container,
                username_param=username,
            )

        if selfhosted_presence:
            typer.echo(__("Connecting to self-hosted instance..."))

            self.__instance_service.connect_to_selfhosted_instance(
                config=config,
                selfhosted_instance_slug=uid,
                username=username,
            )
