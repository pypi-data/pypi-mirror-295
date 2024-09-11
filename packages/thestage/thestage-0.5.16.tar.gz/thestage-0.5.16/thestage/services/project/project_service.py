from typing import Optional

import click
import typer
from git import Commit
from thestage_core.entities.config_entity import ConfigEntity
from thestage_core.services.filesystem_service import FileSystemServiceCore

from thestage.entities.enums.yes_no_response import YesOrNoResponse
from thestage.exceptions.git_access_exception import GitAccessException
from thestage.i18n.translation import __
from thestage.services.clients.git.git_client import GitLocalClient
from thestage.services.clients.thestage_api.dtos.paginated_entity_list import PaginatedEntityList
from thestage.services.clients.thestage_api.dtos.project_controller.project_run_task_response import \
    ProjectRunTaskResponse
from thestage.services.clients.thestage_api.dtos.project_response import ProjectDto
from thestage.services.project.dto.commit_question_response import CommitQuestionResponse
from thestage.services.task.dto.task_dto import TaskDto
from thestage.services.project.dto.project_config import ProjectConfig
from thestage.services.project.mapper.project_task_mapper import ProjectTaskMapper
from thestage.services.remote_server_service import RemoteServerService
from thestage.services.abstract_service import AbstractService
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.config_provider.config_provider import ConfigProvider


class ProjectService(AbstractService):
    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
            remote_server_service: RemoteServerService,
            file_system_service: FileSystemServiceCore,
            git_local_client: GitLocalClient,
    ):
        super(ProjectService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client
        self.__remote_server_service = remote_server_service
        self.__file_system_service = file_system_service
        self.__git_local_client = git_local_client
        self.__project_task_mapper = ProjectTaskMapper()
        self.__config_provider = config_provider

    @error_handler()
    def get_project_by_slug_and_check_if_present(
            self,
            config: ConfigEntity,
            project_slug: Optional[str] = None,
    ) -> Optional[ProjectDto]:
        if not project_slug:
            typer.echo(__('Please go to site and create new project or select present'))
            project_slug: str = typer.prompt(
                text=__('Please give me sketch slug'),
                show_choices=False,
                type=str,
                show_default=False,
            )
            if not project_slug:
                typer.echo(__('Slug can not be empty'))
                raise typer.Exit(1)

        project: Optional[ProjectDto] = self.__thestage_api_client.get_project_by_slug(
            slug=project_slug,
            token=config.main.thestage_auth_token,
        )

        if not project:
            typer.echo(__('You entered the wrong slug, sketch not found'))
            raise typer.Exit(1)

        return project

    @error_handler()
    def init_project(
            self,
            config: ConfigEntity,
            project_slug: str,
    ):
        project = self.get_project_by_slug_and_check_if_present(
            config=config,
            project_slug=project_slug,
        )

        is_git_folder = self.__git_local_client.is_present_local_git(
            path=config.runtime.working_directory,
        )
        if is_git_folder:
            has_remote = self.__git_local_client.has_remote(
                path=config.runtime.working_directory,
            )
            if has_remote:
                typer.echo(__('You have local repo with remote, we can not work with this'))
                raise typer.Exit(1)

        if not project.git_repository_url:
            typer.echo(__('Sketch dont have git repository url'))
            raise typer.Exit(1)

        if project.last_commit_hash or project.last_commit_description:
            prompt_choices = click.Choice(['YES', 'NO'])
            continue_with_non_empty_repo: YesOrNoResponse = typer.prompt(
                text=__('Remote repository is probably not empty: latest commit is "{commit_description}" (sha: {commit_hash})\nDo you wish to continue?').format(commit_description=project.last_commit_description, commit_hash=project.last_commit_hash),
                show_choices=True,
                default=YesOrNoResponse.YES.value,
                type=prompt_choices,
                show_default=True,
            )
            if continue_with_non_empty_repo == "NO":
                typer.echo(__('Project init aborted'))
                raise typer.Exit(0)

        deploy_ssh_key = self.__thestage_api_client.get_project_deploy_ssh_key(
            slug=project.slug,
            token=config.main.thestage_auth_token
        )

        deploy_key_path = self.__config_provider.save_project_deploy_ssh_key(
            deploy_ssh_key=deploy_ssh_key,
            slug=project.slug
        )

        if is_git_folder:
            has_changes = self.__git_local_client.has_changes(
                path=config.runtime.working_directory,
            )
            if has_changes:
                typer.echo(__('You local repo has changes and not empty, please create empty folder'))
                raise typer.Exit(1)
        else:
            repo = self.__git_local_client.init_repository(
                path=config.runtime.working_directory,
            )

        is_remote_added = self.__git_local_client.add_remote_to_repo(
            path=config.runtime.working_directory,
            remote_url=project.git_repository_url,
            remote_name=project.git_repository_name,
        )
        if not is_remote_added:
            typer.echo(__('We can not add remote, something wrong'))
            raise typer.Exit(2)

        self.__git_local_client.git_fetch(path=config.runtime.working_directory, deploy_key_path=deploy_key_path)

        branch = self.__git_local_client.find_main_branch_name(path=config.runtime.working_directory, )
        if branch:
            self.__git_local_client.git_pull(path=config.runtime.working_directory, deploy_key_path=deploy_key_path,
                                             branch=branch)

        self.__git_local_client.init_gitignore(path=config.runtime.working_directory)

        self.__git_local_client.git_add_all(repo_path=config.runtime.working_directory)

        project_config = ProjectConfig()
        project_config.id = project.id
        project_config.slug = project.slug
        project_config.git_repository_url = project.git_repository_url
        project_config.deploy_key_path = str(deploy_key_path)
        self.__config_provider.save_project_config(project_config=project_config)

    @error_handler()
    def clone_project(
            self,
            config: ConfigEntity,
            project_slug: str,
    ):
        if not self.__file_system_service.is_folder_empty(folder=config.runtime.working_directory, auto_create=True):
            typer.echo(__("Cannot clone: the folder is not empty"))
            raise typer.Exit(1)

        project = self.get_project_by_slug_and_check_if_present(
            config=config,
            project_slug=project_slug,
        )

        is_git_folder = self.__git_local_client.is_present_local_git(
            path=config.runtime.working_directory,
        )

        if is_git_folder:
            typer.echo(__('You have local repo, we can not work with this'))
            raise typer.Exit(1)

        if not project.git_repository_url:
            typer.echo(__("Unexpected Project error, missing Repository"))
            raise typer.Exit(1)

        deploy_ssh_key = self.__thestage_api_client.get_project_deploy_ssh_key(slug=project.slug,
                                                                               token=config.main.thestage_auth_token)
        deploy_key_path = self.__config_provider.save_project_deploy_ssh_key(deploy_ssh_key=deploy_ssh_key,
                                                                             slug=project.slug)

        try:
            self.__git_local_client.clone(
                url=project.git_repository_url,
                path=config.runtime.working_directory,
                deploy_key_path=deploy_key_path
            )
            self.__git_local_client.init_gitignore(path=config.runtime.working_directory)
        except GitAccessException as ex:
            typer.echo(ex.get_message())
            typer.echo(ex.get_dop_message())
            typer.echo(__(
                "Please check you mail or open this repo url %git_url% and 'Accept invitation'",
                {
                    'git_url': ex.get_url()
                }
            ))
            raise typer.Exit(1)

        project_config = ProjectConfig()
        project_config.id = project.id
        project_config.slug = project.slug
        project_config.git_repository_url = project.git_repository_url
        project_config.deploy_key_path = str(deploy_key_path)
        self.__config_provider.save_project_config(project_config=project_config)

    @error_handler()
    def project_run_task(
            self,
            config: ConfigEntity,
            project_config: ProjectConfig,
            run_command: str,
            task_title: Optional[str] = None,
            commit_hash: Optional[str] = None,
            task_description: Optional[str] = None,
            docker_container_slug: Optional[str] = None,
    ) -> Optional[TaskDto]:
        if not commit_hash:
            is_git_folder = self.__git_local_client.is_present_local_git(path=config.runtime.working_directory)
            if not is_git_folder:
                typer.echo(__("This folder dont have git project"))
                raise typer.Exit(1)

            self.__git_local_client.git_add_all(repo_path=config.runtime.working_directory)

            has_changes = self.__git_local_client.has_changes(
                path=config.runtime.working_directory,
            )
            if has_changes:
                branch_name = self.__git_local_client.get_active_branch_name(config.runtime.working_directory)
                diff_stat = self.__git_local_client.git_diff_stat(repo_path=config.runtime.working_directory)
                typer.echo(__('Active branch [%branch_name%] has uncommitted changes: %diff_stat_bottomline%', {
                    'diff_stat_bottomline': diff_stat,
                    'branch_name': branch_name,
                }))

                response: str = typer.prompt(
                    text=__('Commit changes? Y/N?'),
                    show_choices=True,
                    default=CommitQuestionResponse.YES.value,
                    type=str,
                    show_default=True,
                )
                if response.upper() == CommitQuestionResponse.NO.value:
                    raise typer.Exit(0)

                commit_name = typer.prompt(
                    text=__('Please provide commit message'),
                    show_choices=False,
                    type=str,
                    show_default=False,
                )

                if commit_name:
                    task_title = task_title if task_title else commit_name
                    commit_result = self.__git_local_client.commit_local_changes(
                        path=config.runtime.working_directory,
                        name=commit_name
                    )

                    if commit_result:
                        # in docs not Commit object, on real - str
                        if isinstance(commit_result, str):
                            typer.echo(commit_result)

                    self.__git_local_client.push_changes(
                        path=config.runtime.working_directory,
                        deploy_key_path=project_config.deploy_key_path
                    )
                    typer.echo(__("Pushed changes to remote repository"))
                else:
                    typer.echo(__('Cannot commit with empty commit name, your code run without last changes.'))

            commit = self.__git_local_client.get_current_commit(path=config.runtime.working_directory)
            if commit and isinstance(commit, Commit):
                commit_hash = commit.hexsha

        if not task_title:
            typer.echo(__("Please provide task title"))

            auto_title = "Task for project {slug}".format(slug=project_config.slug)
            title: str = typer.prompt(
                text=__('New task title:'),
                show_choices=False,
                default=auto_title,
                type=str,
                show_default=True,
            )
            if not title:
                typer.echo(__("Task title can not be empty"))
                raise typer.Exit(1)
            else:
                task_title = title

        run_task_response: ProjectRunTaskResponse = self.__thestage_api_client.execute_project_task(
            token=config.main.thestage_auth_token,
            project_slug=project_config.slug,
            docker_container_slug=docker_container_slug,
            run_command=run_command,
            commit_hash=commit_hash,
            task_title=task_title,
            task_description=task_description,
        )
        if run_task_response:
            if run_task_response.message:
                typer.echo(run_task_response.message)
            if run_task_response.is_success and run_task_response.task:
                typer.echo(__("Task has been scheduled successfully. Task ID: %task_id%", {'task_id': str(run_task_response.task.id)}))
                return run_task_response.task
            else:
                typer.echo(__(
                    'The task failed with an error: %server_massage%',
                    {'server_massage': run_task_response.message or ""}
                ))
                raise typer.Exit(1)
        else:
            typer.echo(__("The task failed with an error"))
            raise typer.Exit(1)

    @error_handler()
    def get_project_task_list(
            self,
            config: ConfigEntity,
            project_slug: str,
            row: int = 5,
            page: int = 1,
    ) -> PaginatedEntityList[TaskDto]:
        data: Optional[PaginatedEntityList[TaskDto]] = self.__thestage_api_client.get_task_list_for_project(
            token=config.main.thestage_auth_token,
            project_slug=project_slug,
            page=page,
            limit=row,
        )

        return data
