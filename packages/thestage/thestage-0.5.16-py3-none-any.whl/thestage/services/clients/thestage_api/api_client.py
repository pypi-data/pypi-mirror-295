from typing import Optional, List, Tuple, Dict, Iterator

import requests
from thestage_core.services.clients.thestage_api.api_client import TheStageApiClientCore

from thestage.services.clients.thestage_api.dtos.docker_container_controller.docker_container_list_request import \
    DockerContainerListRequest
from thestage.services.clients.thestage_api.dtos.docker_container_controller.docker_container_list_response import \
    DockerContainerListResponse
from thestage.services.clients.thestage_api.dtos.entity_filter_request import EntityFilterRequest
from thestage.services.clients.thestage_api.dtos.logging_controller.docker_container_log_stream_request import \
    DockerContainerLogStreamRequest
from thestage.services.clients.thestage_api.dtos.logging_controller.task_log_stream_request import TaskLogStreamRequest
from thestage.services.clients.thestage_api.dtos.paginated_entity_list import PaginatedEntityList
from thestage.services.clients.thestage_api.dtos.project_controller.project_get_deploy_ssh_key_request import \
    ProjectGetDeploySshKeyRequest
from thestage.services.clients.thestage_api.dtos.project_controller.project_get_deploy_ssh_key_response import \
    ProjectGetDeploySshKeyResponse
from thestage.services.clients.thestage_api.dtos.project_controller.project_run_task_request import \
    ProjectRunTaskRequest
from thestage.services.clients.thestage_api.dtos.project_controller.project_run_task_response import \
    ProjectRunTaskResponse
from thestage.services.clients.thestage_api.dtos.project_response import ProjectDto, ProjectViewResponse
from thestage.services.clients.thestage_api.dtos.selfhosted_instance_response import SelfHostedInstanceListResponse, \
    SelfHostedInstanceDto, SelfHostedRentedItemResponse, SelfHostedRentedRentedBusinessStatusMapperResponse
from thestage.services.clients.thestage_api.dtos.container_param_request import DockerContainerActionRequestDto
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto, \
    DockerContainerViewResponse, ContainerBusinessStatusMapperResponse
from thestage.entities.enums.order_direction_type import OrderDirectionType
from thestage.services.clients.thestage_api.dtos.task_controller.task_list_for_project_request import \
    TaskListForProjectRequest
from thestage.services.clients.thestage_api.dtos.task_controller.task_list_for_project_response import \
    TaskListForProjectResponse
from thestage.services.clients.thestage_api.dtos.task_controller.task_status_localized_map_response import \
    TaskStatusLocalizedMapResponse
from thestage.services.clients.thestage_api.dtos.task_controller.task_view_response import TaskViewResponse
from thestage.services.clients.thestage_api.dtos.user_profile import UserProfileResponse
from thestage.services.clients.thestage_api.dtos.instance_rented_response import InstanceRentedListResponse, \
    InstanceRentedDto, InstanceRentedItemResponse, InstanceRentedBusinessStatusMapperResponse

from thestage.services.clients.thestage_api.dtos.base_response import TheStageBaseResponse, \
    TheStageBasePaginatedResponse
from thestage.services.task.dto.task_dto import TaskDto


class TheStageApiClient(TheStageApiClientCore):
    def __init__(self, api_url: str, timeout: int = 90):
        super().__init__(timeout=timeout, url=api_url)

    def get_task(
            self,
            token: str,
            task_id: int,
    ) -> Optional[TaskViewResponse]:
        data = {
            "taskId": task_id,
        }

        response = self._request(
            method='POST',
            url='/user-api/v1/task/view',
            data=data,
            token=token,
        )

        result = TaskViewResponse.model_validate(response) if response else None
        return result if result and result.is_success else None

    def get_task_list_for_project(
            self,
            token: str,
            project_slug: str,
            page: int = 1,
            limit: int = 10,
    ) -> Optional[PaginatedEntityList[TaskDto]]:
        request = TaskListForProjectRequest(
            projectSlug=project_slug,
            entityFilterRequest=EntityFilterRequest(
                orderByField="id",
                orderByDirection=OrderDirectionType.DESC,
                page=page,
                limit=limit,
            ),
        )

        response = self._request(
            method='POST',
            url='/user-api/v1/task/list-for-project',
            data=request.model_dump(),
            token=token,
        )

        result = TaskListForProjectResponse.model_validate(response) if response else None
        return result.tasks if result and result.is_success else None


    def get_rented_instance_list(
            self,
            token: str,
            statuses: List[str],
            query: Optional[str] = None,
            page: int = 1,
            limit: int = 10,
    ) -> PaginatedEntityList[InstanceRentedDto]:
        data = {
            #"statuses": [item.value for item in statuses],
            "entityFilterRequest": {
                "orderByField": "id",
                "orderByDirection": "DESC",
                "page": page,
                "limit": limit
            },
            "queryString": query
        }

        if statuses:
            data['businessStatuses'] = statuses

        response = self._request(
            method='POST',
            url='/user-api/v1/instance-rented/list',
            data=data,
            token=token,
        )

        result = InstanceRentedListResponse.model_validate(response) if response else None
        return result.paginated_list if result and result.paginated_list else ([], None)

    def get_rented_business_status_map(self, token: str, ) -> Optional[Dict[str, str]]:
        response = self._request(
            method='POST',
            url='/user-api/v1/instance-rented/business-status-localized-map',
            data=None,
            token=token,
        )

        data = InstanceRentedBusinessStatusMapperResponse.model_validate(response) if response else None

        return data.instance_rented_business_status_map if data else None

    def get_task_localized_status_map(self, token: str, ) -> Optional[Dict[str, str]]:
        response = self._request(
            method='POST',
            url='/user-api/v1/task/status-localized-mapping',
            data=None,
            token=token,
        )

        data = TaskStatusLocalizedMapResponse.model_validate(response) if response else None

        return data.taskStatusMap if data else None

    def get_rented_item(
            self,
            token: str,
            instance_slug: Optional[str] = None,
            instance_id: Optional[int] = None,
    ) -> Optional[InstanceRentedDto]:
        if not instance_slug and not instance_id:
            return None

        data = {
            "instanceRentedSlug": instance_slug,
        }

        response = self._request(
            method='POST',
            url='/user-api/v1/instance-rented/view-by-slug',
            data=data,
            token=token,
        )

        return InstanceRentedItemResponse.model_validate(response).instance_rented if response else None

    def get_selfhosted_item(
            self,
            token: str,
            instance_slug: Optional[str] = None,
            instance_id: Optional[int] = None,
    ) -> Optional[SelfHostedInstanceDto]:
        if not instance_slug and not instance_id:
            return None

        data = {
            "selfhostedInstanceSlug": instance_slug,
        }

        response = self._request(
            method='POST',
            url='/user-api/v1/self-hosted-instance/view-by-slug',
            data=data,
            token=token,
        )

        return SelfHostedRentedItemResponse.model_validate(response).selfhosted_instance if response else None

    def get_selfhosted_instance_list(
            self,
            token: str,
            statuses: List[str],
            query: Optional[str] = None,
            page: int = 1,
            limit: int = 10,
    ) -> PaginatedEntityList[SelfHostedInstanceDto]:
        data = {
            #"statuses": [item.value for item in statuses] if statuses else [],
            "entityFilterRequest": {
                "orderByField": "id",
                "orderByDirection": "DESC",
                "page": page,
                "limit": limit
            },
            "queryString": query
        }

        if statuses:
            data['businessStatuses'] = statuses

        response = self._request(
            method='POST',
            url='/user-api/v1/self-hosted-instance/list',
            data=data,
            token=token,
        )

        result = SelfHostedInstanceListResponse.model_validate(response) if response else None
        return result.paginated_list if result and result.paginated_list else ([], None)

    def get_selfhosted_business_status_map(self, token: str, ) -> Optional[Dict[str, str]]:
        response = self._request(
            method='POST',
            url='/user-api/v1/self-hosted-instance/business-status-localized-map',
            data=None,
            token=token,
        )

        data = SelfHostedRentedRentedBusinessStatusMapperResponse.model_validate(response) if response else None
        return data.selfhosted_instance_business_status_map if data else None

    def get_profile(
            self,
            token: str,
    ) -> Optional[UserProfileResponse]:

        response = self._request(
            method='GET',
            url='/frontend-api/user/my-profile',
            token=token,
        )

        result = UserProfileResponse.model_validate(response) if response else None
        return result if result else None

    def stop_task_on_instance(
            self,
            token: str,
            task_id: int,
    ) -> Optional[TheStageBaseResponse]:
        data = {
            "taskId": task_id,
        }

        response = self._request(
            method='POST',
            url='/user-api/v1/task/cancel-task',
            data=data,
            token=token,
        )

        result = TheStageBaseResponse.model_validate(response) if response else None
        return result if result else None

    def get_container_list(
            self,
            token: str,
            query_string: Optional[str] = None,
            instance_rented_id: Optional[int] = None,
            selfhosted_instance_id: Optional[int] = None,
            project_id: Optional[int] = None,
            statuses: List[str] = [],
            page: int = 1,
            limit: int = 10,
    ) -> PaginatedEntityList[DockerContainerDto]:
        request = DockerContainerListRequest(
            statuses=statuses,
            entityFilterRequest=EntityFilterRequest(
                orderByField="id",
                orderByDirection=OrderDirectionType.DESC,
                page=page,
                limit=limit,
            ),
        )

        response = self._request(
            method='POST',
            url='/user-api/v1/docker-container/list',
            data=request.model_dump(),
            token=token,
        )

        result = DockerContainerListResponse.model_validate(response) if response else None
        # return result.paginatedList.entities, result.paginatedList.pagination_data.total_pages if result and result.is_success else None
        return result.paginatedList if result and result.is_success else None

    def get_container(
            self,
            token: str,
            container_slug: Optional[str] = None,
            container_id: Optional[int] = None,
    ) -> Optional[DockerContainerDto]:
        if not container_slug and not container_id:
            return None

        if container_id:
            data = {
                "dockerContainerId": container_id,
            }
        else:
            data = {
                "dockerContainerSlug": container_slug,
            }

        response = self._request(
            method='POST',
            url='/user-api/v1/docker-container/view',
            data=data,
            token=token,
        )

        return DockerContainerViewResponse.model_validate(response).docker_container if response else None

    def container_action(
            self,
            token: str,
            request_param: DockerContainerActionRequestDto,
    ) -> bool:

        response = self._request(
            method='POST',
            url='/user-api/v1/docker-container/action',
            data=request_param.model_dump(by_alias=True),
            token=token,
        )

        result = TheStageBasePaginatedResponse.model_validate(response) if response else None
        return result.is_success if result and result.is_success else False

    def get_container_business_status_map(self, token: str, ) -> Optional[Dict[str, str]]:
        response = self._request(
            method='POST',
            url='/user-api/v1/docker-container/status-localized-mapping',
            data=None,
            token=token,
        )

        data = ContainerBusinessStatusMapperResponse.model_validate(response) if response else None
        return data.docker_container_status_map if data else None

    def get_project_by_slug(self, slug: str, token: str) -> Optional[ProjectDto]:
        data = {
            "projectSlug": slug,
        }

        response = self._request(
            method='POST',
            url='/user-api/v1/project/view-by-slug',
            data=data,
            token=token,
        )

        result = ProjectViewResponse.model_validate(response) if response else None
        project = ProjectDto.model_validate(result.project) if result else None
        return project if result and result.is_success else None

    def get_project_deploy_ssh_key(self, slug: str, token: str) -> str:
        request = ProjectGetDeploySshKeyRequest(
            projectSlug=slug
        )

        response = self._request(
            method='POST',
            url='/user-api/v1/project/get-deploy-ssh-key',
            data=request.model_dump(),
            token=token,
        )

        result = ProjectGetDeploySshKeyResponse.model_validate(response) if response else None
        return result.privateKey if result and result.is_success else None

    def execute_project_task(
            self,
            token: str,
            project_slug: str,
            run_command: str,
            task_title: str,
            docker_container_slug: Optional[str] = None,
            commit_hash: Optional[str] = None,
            task_description: Optional[str] = None,
    ) -> Optional[ProjectRunTaskResponse]:
        request = ProjectRunTaskRequest(
            projectSlug=project_slug,
            dockerContainerSlug=docker_container_slug,
            commitHash=commit_hash,
            runCommand=run_command,
            taskTitle=task_title,
            taskDescription=task_description,
        )

        response = self._request(
            method='POST',
            url='/user-api/v1/project/execute-task',
            data=request.model_dump(),
            token=token,
        )

        return ProjectRunTaskResponse.model_validate(response) if response else None

    def get_container_log_stream(self, token: str, container_id: int) -> Iterator[str]:
        request_headers = {'Content-Type': 'application/json'}
        if token: request_headers['Authorization'] = f"Bearer {token}"

        session = requests.Session()
        request = DockerContainerLogStreamRequest(
            dockerContainerId=container_id,
        )

        with session.post(
            url=f"{self._get_host()}/user-api/v1/logging/stream/container",
            headers=request_headers,
            stream=True,
            json=request.model_dump(),
        ) as response:
            for line in response.iter_lines():
                if line:
                    yield line.decode('utf-8')

    def get_task_log_stream(self, token: str, task_id: int) -> Iterator[str]:
        request_headers = {'Content-Type': 'application/json'}
        if token: request_headers['Authorization'] = f"Bearer {token}"

        session = requests.Session()
        request = TaskLogStreamRequest(
            taskId=task_id,
        )

        with session.post(
                url=f"{self._get_host()}/user-api/v1/logging/stream/task",
                headers=request_headers,
                stream=True,
                json=request.model_dump(),
        ) as response:
            for line in response.iter_lines():
                if line:
                    yield line.decode('utf-8')
