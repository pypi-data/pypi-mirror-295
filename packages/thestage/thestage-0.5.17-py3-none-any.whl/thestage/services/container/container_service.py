import uuid
from typing import List, Tuple, Optional, Dict

import typer
from thestage_core.entities.config_entity import ConfigEntity
from thestage_core.entities.file_item import FileItemEntity
from thestage_core.services.filesystem_service import FileSystemServiceCore

from thestage.helpers.logger.app_logger import app_logger
from thestage.services.clients.thestage_api.dtos.container_param_request import DockerContainerActionRequestDto
from thestage.services.clients.thestage_api.dtos.enums.container_pending_action import ContainerPendingActionEnumDto
from thestage.services.clients.thestage_api.dtos.enums.container_status import DockerContainerStatus
from thestage.entities.enums.shell_type import ShellType
from thestage.services.clients.thestage_api.dtos.paginated_entity_list import PaginatedEntityList
from thestage.services.clients.thestage_api.dtos.sftp_path_helper import SftpFileItemEntity
from thestage.services.remote_server_service import RemoteServerService
from thestage.i18n.translation import __
from thestage.services.abstract_service import AbstractService
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.config_provider.config_provider import ConfigProvider


class ContainerService(AbstractService):

    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
            remote_server_service: RemoteServerService,
            file_system_service: FileSystemServiceCore,
    ):
        super(ContainerService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client
        self.__remote_server_service = remote_server_service
        self.__file_system_service = file_system_service

    @error_handler()
    def get_list(
            self,
            config: ConfigEntity,
            statuses: List[str],
            row: int = 5,
            page: int = 1,
    ) -> PaginatedEntityList[DockerContainerDto]:

        list = self.__thestage_api_client.get_container_list(
            token=config.main.thestage_auth_token,
            statuses=statuses,
            page=page,
            limit=row,
        )

        return list

    @error_handler()
    def get_container(
            self,
            config: ConfigEntity,
            container_id: Optional[int] = None,
            container_slug: Optional[str] = None,
    ) -> Optional[DockerContainerDto]:
        return self.__thestage_api_client.get_container(
            token=config.main.thestage_auth_token,
            container_id=container_id,
            container_slug=container_slug,
        )

    @staticmethod
    def get_server_auth(
            container: DockerContainerDto,
            username_param: Optional[str] = None,
    ) -> Tuple[str, str]:
        if container.instance_rented:
            username = container.instance_rented.host_username
            ip_address = container.instance_rented.ip_address
        elif container.selfhosted_instance:
            username = container.selfhosted_instance.host_username or 'root'
            ip_address = container.selfhosted_instance.ip_address
        else:
            typer.echo(__("Neither rented nor self-hosted server instance found to connect to"))
            raise typer.Exit(1)

        if not username_param:
            if not username:
                username = typer.prompt(
                    default='ubuntu',
                    text=__('Provide  username to connect to server instance'),
                    show_choices=False,
                    type=str,
                    show_default=True,
                )
        else:
            username = username_param

        return username, ip_address

    @error_handler()
    def connect_container(
            self,
            config: ConfigEntity,
            container: DockerContainerDto,
            username_param: Optional[str] = None,
    ):

        username, ip_address = self.get_server_auth(
            container=container,
            username_param=username_param,
        )

        if not container.system_name:
            typer.echo(__("Unable to connect to container: container system_name is missing"))
            raise typer.Exit(1)

        shell: Optional[ShellType] = self.__remote_server_service.get_shell_from_container(
            ip_address=ip_address,
            username=username,
            docker_name=container.system_name,
        )

        if not shell:
            typer.echo(__("Failed to start shell (bash, sh) in container: ensure compatible shell is available"))
            raise typer.Exit(1)

        self.__remote_server_service.connect_to_container(
            ip_address=ip_address,
            username=username,
            docker_name=container.system_name,
            shell=shell,
        )

    @error_handler()
    def check_container_status_for_start(
            self,
            container: DockerContainerDto,
    ) -> DockerContainerDto:
        if container:
            if container.frontend_status.status_key == DockerContainerStatus.RUNNING:
                typer.echo(__('Container is already running'))
                raise typer.Exit(1)
            elif container.frontend_status.status_key == DockerContainerStatus.CREATING:
                typer.echo(__('Container is being created'))
                raise typer.Exit(1)
            elif container.frontend_status.status_key in [
                DockerContainerStatus.STARTING,
                DockerContainerStatus.RESTARTING,
            ]:
                typer.echo(__('Container is starting'))
                raise typer.Exit(1)
            elif container.frontend_status.status_key in [
                DockerContainerStatus.DELETING,
                DockerContainerStatus.DELETED,
            ]:
                typer.echo(__('Container has been deleted'))
                raise typer.Exit(1)

        return container

    @error_handler()
    def check_container_status_for_stop(
            self,
            container: DockerContainerDto,
    ) -> DockerContainerDto:
        if container:
            if container.frontend_status.status_key in [
                DockerContainerStatus.CREATING,
                DockerContainerStatus.STARTING,
                DockerContainerStatus.RESTARTING,
            ]:
                typer.echo(__('Container is being created, started, or restarted'))
                raise typer.Exit(1)
            elif container.frontend_status.status_key in [
                DockerContainerStatus.FAILED,
                DockerContainerStatus.DEAD,
                DockerContainerStatus.CREATING_FAILED,
                DockerContainerStatus.STOPPING,
                DockerContainerStatus.STOPPED,
            ]:
                typer.echo(__('Container is already stopped'))
                raise typer.Exit(1)
            elif container.frontend_status.status_key in [
                DockerContainerStatus.DELETING,
                DockerContainerStatus.DELETED,
            ]:
                typer.echo(__('Container has been deleted'))
                raise typer.Exit(1)

        return container

    @error_handler()
    def check_container_status_for_work(
            self,
            container: DockerContainerDto,
    ) -> DockerContainerDto:
        if container:
            if container.frontend_status.status_key in [
                DockerContainerStatus.CREATING.value,
                DockerContainerStatus.STARTING.value,
                DockerContainerStatus.RESTARTING.value,
            ]:
                typer.echo(__('Container is restarting'))
                raise typer.Exit(1)
            elif container.frontend_status.status_key in [
                DockerContainerStatus.FAILED.value,
                DockerContainerStatus.DEAD.value,
                DockerContainerStatus.CREATING_FAILED.value,
                DockerContainerStatus.STOPPING.value,
                DockerContainerStatus.STOPPED.value,
            ]:
                typer.echo(__('Container has failed, start it again'))
                raise typer.Exit(1)
            elif container.frontend_status.status_key in [
                DockerContainerStatus.DELETING.value,
                DockerContainerStatus.DELETED.value,
            ]:
                typer.echo(__('Container has been deleted'))
                raise typer.Exit(1)

        return container

    @staticmethod
    def _get_new_path_from_mapping(
            directory_mapping: Dict[str, str],
            destination_path: str,
    ) -> Tuple[Optional[str], Optional[str]]:

        instance_path: Optional[str] = None
        container_path: Optional[str] = None

        for instance_mapping, container_mapping in directory_mapping.items():
            if destination_path.startswith(f"{container_mapping}/") or destination_path == container_mapping:
                instance_path = destination_path.replace(container_mapping, instance_mapping)
                container_path = destination_path
                # dont break, check all mapping list

        if instance_path and container_path:
            return instance_path, container_path
        else:
            return None, None

    def __build_local_path_by_mapping(
            self,
            files: List[FileItemEntity],
            instance_path: str,
            container_path: str,
            destination_path: str,
            with_tmp: bool = False,
            has_parent: bool = False,
    ):
        result = []
        for item in files:
            elem = SftpFileItemEntity.model_validate(item.model_dump())
            if item.is_file:
                has_file_name = self.__remote_server_service._check_if_file_name_in_path(
                    path=instance_path,
                    file_template=item.name,
                )

                if not has_parent and not with_tmp and has_file_name:
                    elem.instance_path = instance_path
                    elem.container_path = container_path
                else:
                    elem.instance_path = f"{instance_path}/{item.name}"
                    elem.container_path = f"{container_path}/{item.name}"

                if with_tmp:
                    has_file_name = self.__remote_server_service._check_if_file_name_in_path(
                        path=destination_path,
                        file_template=item.name,
                    )
                    if has_file_name:
                        elem.dest_path = destination_path
                    else:
                        elem.dest_path = f"{destination_path}/{item.name}"
                else:
                    elem.dest_path = elem.instance_path

            else:
                if not has_parent and not with_tmp:
                    elem.instance_path = instance_path
                    elem.container_path = container_path
                else:
                    elem.instance_path = f"{instance_path}/{item.name}"
                    elem.container_path = f"{container_path}/{item.name}"

                if with_tmp:
                    elem.dest_path = destination_path
                else:
                    elem.dest_path = elem.instance_path

            if len(item.children) > 0:
                elem.children = []
                elem.children.extend(self.__build_local_path_by_mapping(
                    files=item.children,
                    instance_path=elem.instance_path,
                    container_path=elem.container_path,
                    destination_path=elem.dest_path,
                    with_tmp=with_tmp,
                    has_parent=True,
                ))

            result.append(elem)

        return result

    @error_handler()
    def put_file_to_container(
            self,
            container: DockerContainerDto,
            src_path: str,
            copy_only_folder_contents: bool,
            destination_path: Optional[str] = None,
            username_param: Optional[str] = None,
    ):

        username, ip_address = self.get_server_auth(
            container=container,
            username_param=username_param,
        )

        if not self.__file_system_service.check_if_path_exist(file=src_path):
            typer.echo(__("File not found at specified path"))
            raise typer.Exit(1)

        if not container.mappings or not container.mappings.directory_mappings:
            typer.echo(__("Mapping folders not found"))
            raise typer.Exit(1)

        instance_path, container_path = self._get_new_path_from_mapping(
            directory_mapping=container.mappings.directory_mappings,
            destination_path=destination_path,
        )

        if not instance_path and not container_path:
            typer.echo(__("Cannot find matching container volume mapping for specified file path"))
            raise typer.Exit(1)

        self.__remote_server_service.upload_data_to_container(
            ip_address=ip_address,
            username=username,
            docker_name=container.system_name,
            src_path=src_path,
            dest_path=destination_path,
            instance_path=instance_path,
            container_path=container_path,
            is_folder=self.__file_system_service.is_folder(folder=src_path, auto_create=False, with_exception=False),
            copy_only_folder_contents=copy_only_folder_contents
        )

    @error_handler()
    def get_file_from_container(
            self,
            container: DockerContainerDto,
            src_path: str,
            copy_only_folder_contents: bool,
            destination_path: Optional[str] = None,
            username_param: Optional[str] = None,
    ):
        username, ip_address = self.get_server_auth(
            container=container,
            username_param=username_param,
        )

        if not container.mappings or not container.mappings.directory_mappings:
            typer.echo(__("Mapping folders not found"))
            raise typer.Exit(1)

        instance_path, container_path = self._get_new_path_from_mapping(
            directory_mapping=container.mappings.directory_mappings,
            destination_path=src_path,
        )

        if not instance_path and not container_path:
            typer.echo(__("Cannot find matching container volume mapping for specified file path"))
            raise typer.Exit(1)

        self.__remote_server_service.download_data_from_container(
            ip_address=ip_address,
            username=username,
            dest_path=destination_path,
            instance_path=instance_path,
            copy_only_folder_contents=copy_only_folder_contents
        )

    @error_handler()
    def change_container_status(
            self,
            config: ConfigEntity,
            container: DockerContainerDto,
            action: ContainerPendingActionEnumDto,
    ) -> bool:
        request_params = DockerContainerActionRequestDto(
            dockerContainerId=container.id,
            action=action,
        )
        result = self.__thestage_api_client.container_action(
            token=config.main.thestage_auth_token,
            request_param=request_params,
        )
        if not result:
            app_logger.error(f'Container status not changed - {result}')

        return result
