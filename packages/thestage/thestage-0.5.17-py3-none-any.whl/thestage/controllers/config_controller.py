from thestage_core.entities.config_entity import ConfigEntity

from thestage.i18n.translation import __
from thestage.helpers.logger.app_logger import app_logger
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.service_factory import ServiceFactory
from thestage.controllers.utils_controller import get_current_directory, validate_config_and_get_service_factory

import typer

app = typer.Typer(no_args_is_help=True, help=__("Manage configuration settings"))


@app.command(name='get', no_args_is_help=False, help=__("Display all configuration settings"))
def config_get():
    """
        Lists all configuration settings
    """
    app_logger.info(f'Start config from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    if not config:
        typer.echo(__('No configuration found'))
        raise typer.Exit(1)

    typer.echo(__('THESTAGE TOKEN: %token%', {'token': config.main.thestage_auth_token or ''}))
    typer.echo(__('THESTAGE API LINK: %link%', {'link': config.main.thestage_api_url or ''}))
    if config.runtime.config_global_path:
        typer.echo(__('CONFIG PATH: %path%', {'path': str(config.runtime.config_global_path or '')}))

    raise typer.Exit(0)


@app.command(name='set', no_args_is_help=True, help=__("Update configuration settings"))
def config_set(
    token: str = typer.Option(
            None,
            "--api-token",
            "-t",
            help=__("Set or update API token"),
            is_eager=False,
            is_flag=True,
        ),
):
    """
        Updates configuration settings
    """
    app_logger.info(f'Start config from {get_current_directory()}')

    config_provider = ConfigProvider(local_path=get_current_directory())
    service_factory = ServiceFactory(config_provider)

    app_service = service_factory.get_app_config_service()

    if token:
        app_service.app_change_token(config=config_provider.get_full_config(), token=token)

    typer.echo('Configuration updated successfully')
    raise typer.Exit(0)


@app.command(name='clear', no_args_is_help=False, help=__("Clear configuration"))
def config_clear():
    """
        Clears all configuration settings
    """
    app_logger.info(f'Start config from {get_current_directory()}')
    service_factory = validate_config_and_get_service_factory()
    service_factory.get_config_provider().remove_all_config()

    raise typer.Exit(0)
