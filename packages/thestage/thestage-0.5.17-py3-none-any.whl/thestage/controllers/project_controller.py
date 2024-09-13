import os
from typing import Optional, List

from typing_extensions import Annotated

from thestage.services.logging.logging_service import LoggingService
from thestage.services.project.mapper.project_task_mapper import ProjectTaskMapper

from thestage.entities.project_task import ProjectTaskEntity
from thestage.i18n.translation import __
from thestage.services.task.dto.task_dto import TaskDto
from thestage.helpers.logger.app_logger import app_logger
from thestage.controllers.utils_controller import validate_config_and_get_service_factory, get_current_directory

import typer

from thestage.services.project.dto.project_config import ProjectConfig
from thestage.services.project.project_service import ProjectService

app = typer.Typer(no_args_is_help=True, help=__("Manage projects"))

task = typer.Typer(no_args_is_help=True, help=__("Manage project tasks"))
app.add_typer(task, name="task")

@app.command(name='clone', no_args_is_help=True, help=__("Clone project repository to empty directory"))
def clone(
        project_uid: str = typer.Argument(
            help=__("Project unique ID"),
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to the working directory: current directory used by default"),
            is_eager=False,
        ),
):
    """
        Clones project to current working directory
    """
    app_logger.info(f'Start project clone from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()
    # file_system_service = service_factory.get_file_system_service()

    project_service.clone_project(
        config=config,
        project_slug=project_uid,
    )

    typer.echo(__("Project successfully cloned to %path%", {"path": config.runtime.working_directory}))
    raise typer.Exit(0)


@app.command(name='init', no_args_is_help=True, help=__("Initialize project repository with existing files"))
def init(
        project_uid: Optional[str] = typer.Argument(
            help=__("Project unique ID"),
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            is_eager=False,
        ),
):
    """
        Initializes project in current working directory
    """
    app_logger.info(f'Start project init from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()
    project_config = service_factory.get_config_provider().read_project_config()

    if project_config:
        typer.echo(__("Directory is initialized and already contains working project"))
        raise typer.Exit(1)

    project_service.init_project(
        project_slug=project_uid,
        config=config,
    )

    typer.echo(__("Project successfully initialized at %path%", {"path": config.runtime.working_directory}))
    typer.echo(__("Initialization complete"))
    raise typer.Exit(0)


@app.command(name='run', no_args_is_help=True, help=__("Run task within project. By default, it uses the latest commit from the main branch and streams real-time task logs."))
def run(
        command: Annotated[List[str], typer.Argument(
            help=__("Command to run (required)"),
        )],
        commit_hash: Optional[str] = typer.Option(
            None,
            '--commit-hash',
            '-hash',
            help=__("Commit hash to use. By default, the current HEAD commit is used."),
            is_eager=False,
        ),
        task_title: Optional[str] = typer.Option(
            None,
            '--task-title',
            '-t',
            help=__("Task title"),
            is_eager=False,
        ),
        task_description: Optional[str] = typer.Option(
            None,
            '--task-description',
            '-d',
            help=__("Task description"),
            is_eager=False,
        ),
        docker_container_slug: Optional[str] = typer.Option(
            None,
            '--container-uid',
            '-cid',
            help=__("Docker container unique ID"),
            is_eager=False,
        ),
        working_directory: Optional[str] = typer.Option(
            None,
            "--working-directory",
            "-wd",
            help=__("Full path to working directory"),
            show_default=False,
            is_eager=False,
        ),
        enable_log_stream: Optional[bool] = typer.Option(
            True,
            " /--no-logs",
            " /-nl",
            help=__("Disable real-time log streaming"),
            is_eager=False,
        ),
):
    """
        Runs a task within a project
    """
    app_logger.info(f'Start project run from {get_current_directory()}')

    if not command:
        typer.echo(__('Command is required'))
        raise typer.Exit(1)

    if not docker_container_slug:
        typer.echo(__('Docker container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(working_directory=working_directory)
    config = service_factory.get_config_provider().get_full_config()

    project_service = service_factory.get_project_service()
    project_config: ProjectConfig = service_factory.get_config_provider().read_project_config()

    if not project_config:
        typer.echo(__("No project found at the path: %path%. Please initialize or clone a project first.", {"path": config.runtime.working_directory}))
        raise typer.Exit(1)

    task: Optional[TaskDto] = project_service.project_run_task(
        config=config,
        project_config=project_config,
        run_command=" ".join(command),
        commit_hash=commit_hash,
        task_title=task_title,
        task_description=task_description,
        docker_container_slug=docker_container_slug,
    )

    if enable_log_stream:
        logging_service: LoggingService = service_factory.get_logging_service()

        logging_service.stream_task_logs(
            config=config,
            task_id=task.id
        )

    raise typer.Exit(0)


@task.command("ls", help=__("List tasks"))
def list_runs(
        project_uid: Annotated[str, typer.Argument(help=__("Project unique ID. By default, project info is taken from the current directory"), metavar="OPTIONAL")] = None,
        row: int = typer.Option(
            5,
            '--row',
            '-r',
            help=__("Set number of rows displayed per page"),
            is_eager=False,
        ),
        page: int = typer.Option(
            1,
            '--page',
            '-p',
            help=__("Set starting page for displaying output"),
            is_eager=False,
        ),
):
    """
        Lists tasks for a project
    """
    app_logger.info(f'Start project list-runs from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    project_service: ProjectService = service_factory.get_project_service()

    if not project_uid:
        project_config: ProjectConfig = service_factory.get_config_provider().read_project_config()
        if not project_config:
            typer.echo(__("Provide the project unique ID or run this command from within an initialized project directory"))
            raise typer.Exit(1)
        project_uid = project_config.slug

    project_service.print(
        func_get_data=project_service.get_project_task_list,
        func_special_params={
            'project_slug': project_uid,
        },
        mapper=ProjectTaskMapper(),
        config=config,
        headers=list(map(lambda x: x.alias, ProjectTaskEntity.model_fields.values())),
        row=row,
        page=page,
        max_col_width=[100, 100, 100, 100, 100, 100, 100, 100],
        show_index="never",
    )

    typer.echo(__("Tasks listing complete"))
    raise typer.Exit(0)


@task.command(name="logs", no_args_is_help=True, help=__("Stream real-time task logs"))
def task_logs(
        task_id: Optional[int] = typer.Argument(help=__("Task ID"),),
):
    """
        Streams real-time task logs
    """
    app_logger.info(f'View task logs')

    if not task_id:
        typer.echo(__('Task ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    logging_service: LoggingService = service_factory.get_logging_service()

    logging_service.stream_task_logs(
        config=config,
        task_id=task_id
    )

    app_logger.info(f'Task logs - end')
    raise typer.Exit(0)
