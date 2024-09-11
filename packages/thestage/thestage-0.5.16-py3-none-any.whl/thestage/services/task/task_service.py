from typing import Optional

from thestage_core.entities.config_entity import ConfigEntity
from thestage.services.abstract_service import AbstractService
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.clients.thestage_api.dtos.task_controller.task_view_response import TaskViewResponse
from thestage.services.config_provider.config_provider import ConfigProvider


class TaskService(AbstractService):

    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
    ):
        super(TaskService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client

    @error_handler()
    def get_task(
            self,
            config: ConfigEntity,
            task_id: Optional[int] = None,
    ) -> Optional[TaskViewResponse]:
        return self.__thestage_api_client.get_task(
            token=config.main.thestage_auth_token,
            task_id=task_id,
        )
