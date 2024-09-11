import os
from pathlib import Path
from typing import Optional

from thestage_core.services.config_provider.config_provider import ConfigProviderCore

from thestage.services.project.dto.project_config import ProjectConfig


class ConfigProvider(ConfigProviderCore):
    def __init__(
            self,
            local_path: str,
    ):
        super(ConfigProvider, self).__init__(
            local_path=local_path,
        )

    def save_project_config(self, project_config: ProjectConfig):
        self.__create_empty_project_config_if_missing()
        # self.read_project_config()
        project_config_path = self.__get_project_config_path(with_file=True)
        self._save_config_file(data=project_config.model_dump(), file_path=project_config_path)

    def save_project_deploy_ssh_key(self, slug: str, deploy_ssh_key: str) -> str:
        deploy_key_dirpath = self._global_config_path.joinpath('project_deploy_keys')
        self._file_system_service.create_if_not_exists(deploy_key_dirpath)

        deploy_key_filepath = deploy_key_dirpath.joinpath('project_deploy_key_' + slug)
        self._file_system_service.create_if_not_exists_file(deploy_key_filepath)

        text_file = open(deploy_key_filepath, "w")
        text_file.write(deploy_ssh_key)
        text_file.close()
        os.chmod(deploy_key_filepath, 0o600)

        return str(deploy_key_filepath)

    def read_project_config(self) -> Optional[ProjectConfig]:
        project_data_dirpath = self.__get_project_config_path()
        if not project_data_dirpath.exists():
            return None
            # self._file_system_service.create_if_not_exists(project_data_dirpath)

        project_data_filepath = self.__get_project_config_path(with_file=True)
        if not project_data_filepath.exists():
            return None

        config_data = self._read_config_file(project_data_filepath) if project_data_filepath and project_data_filepath.exists() else {}
        return ProjectConfig.model_validate(config_data)


    def __create_empty_project_config_if_missing(self):
        project_data_dirpath = self.__get_project_config_path()
        if not project_data_dirpath.exists():
            self._file_system_service.create_if_not_exists(project_data_dirpath)

        project_data_filepath = self.__get_project_config_path(with_file=True)
        if not project_data_filepath.exists():
            self._file_system_service.create_if_not_exists_file(project_data_filepath)


    def __get_project_config_path(self, with_file: bool = False) -> Path:
        if with_file:
            return self._local_config_path.joinpath('project.json')
        else:
            return self._local_config_path