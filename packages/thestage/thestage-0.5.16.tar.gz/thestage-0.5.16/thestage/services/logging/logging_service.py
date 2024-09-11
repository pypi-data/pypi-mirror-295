from typing import Optional, Dict

import typer
from requests.exceptions import ChunkedEncodingError
from thestage_core.entities.config_entity import ConfigEntity

from thestage.services.clients.thestage_api.dtos.enums.task_status import TaskStatus
from thestage.services.clients.thestage_api.dtos.task_controller.task_status_localized_map_response import \
    TaskStatusLocalizedMapResponse
from thestage.services.clients.thestage_api.dtos.task_controller.task_view_response import TaskViewResponse
from thestage.services.task.dto.task_dto import TaskDto
from thestage.services.logging.dto.log_message import LogMessage
from thestage.services.logging.dto.log_type import LogType
from thestage.i18n.translation import __
from thestage.services.abstract_service import AbstractService
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.config_provider.config_provider import ConfigProvider
from rich import print

class LoggingService(AbstractService):
    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
    ):
        super(LoggingService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client

    @error_handler()
    def stream_container_logs(self, config: ConfigEntity, container: DockerContainerDto):
        typer.echo(__(
            f"Log stream for docker container '%container_slug%' started",
            {
                'container_slug': container.slug,
            }
        ))
        typer.echo(__("Press CTRL+C to stop"))
        try:
            for log_json in self.__thestage_api_client.get_container_log_stream(
                    token=config.main.thestage_auth_token,
                    container_id=container.id
            ):
                self.__print_log_line(log_json)
        except ChunkedEncodingError as e1:  # handling server timeout
            typer.echo(__('Log stream disconnected'))
            raise typer.Exit(1)

        typer.echo(__('Log stream disconnected'))

    @error_handler()
    def stream_task_logs(self, config: ConfigEntity, task_id: int):
        task_view_response: Optional[TaskViewResponse] = self.__thestage_api_client.get_task(
            token=config.main.thestage_auth_token,
            task_id=task_id,
        )

        task_status_map: Dict[str, str] = self.__thestage_api_client.get_task_localized_status_map(
            token=config.main.thestage_auth_token,
        )

        task = task_view_response.task

        if task:
            if task.frontend_status.status_key not in [TaskStatus.RUNNING, TaskStatus.SCHEDULED]:
                typer.echo(__("Task must be in status: '%required_status%'. Task %task_id% status: '%status%'", {
                    'task_id': str(task.id),
                    'status': task.frontend_status.status_translation,
                    'required_status': task_status_map.get(TaskStatus.RUNNING) or TaskStatus.RUNNING
                }))
                raise typer.Exit(1)
        else:
            typer.echo(__("Task with ID %task_id% was not found", {'task_id': task.id}))
            raise typer.Exit(1)

        typer.echo(__(
            f"Log stream for task %task_id% started",
            {
                'task_id': str(task.id),
            }
        ))
        typer.echo(__("Press CTRL+C to stop"))
        try:
            for log_json in self.__thestage_api_client.get_task_log_stream(
                    token=config.main.thestage_auth_token,
                    task_id=task.id
            ):
                self.__print_log_line(log_json)
        except ChunkedEncodingError as e1:  # handling server timeout
            typer.echo(__('Log stream disconnected ' + e1))
            raise typer.Exit(1)

        typer.echo(__('Log stream disconnected'))

    @staticmethod
    def __print_log_line(log_message_raw_json: str):
        timestamp_color: str = "#fbcb0a"
        line_color: str = "grey78"
        log_obj = LogMessage.model_validate_json(log_message_raw_json)
        if log_obj.log_type == LogType.stderr:
            line_color = "red"
        if log_obj.message:
            print(f'[not bold][{timestamp_color}][{log_obj.timestamp}][/{timestamp_color}][/not bold][{line_color}][bold][{(log_obj.log_type or "None").upper()}][/bold] [not bold]{log_obj.message}[/not bold][/{line_color}]')
