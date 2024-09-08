from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, SerializeAsAny
from aws_cdk import Environment
from os import getenv, path

from .environment_parameters import BaseAccount, EnvironmentParameters
from .default_settings import DefaultSettings
from .tags import Tags

TAccount = TypeVar('TAccount', bound=BaseAccount)  # EnvironmentParameters extension if we update python to 3.12 we can use DefaultAccount as default
TSettings = TypeVar('TSettings', bound=DefaultSettings)    # Settings model

class ConfigProvider(Generic[TSettings, TAccount]):
    """ This class aggregates all config passed to the CDK App. Config comes from the following sources:
        - environments_parameters, provided by the cloud team
        - settings, provided in the pipeline for each environment
    """
    _instance: Optional["ConfigProvider[TSettings, TAccount]"] = None

    def __new__(cls, environments_parameters: EnvironmentParameters[TAccount], settings: TSettings, relative_path: str = '../'):
        if cls._instance is None:
            cls._instance = super(ConfigProvider, cls).__new__(cls)
            cls._instance.__init_once(environments_parameters, settings, relative_path)
        return cls._instance

    def __init_once(self, environments_parameters: EnvironmentParameters[TAccount], settings: TSettings, relative_path: str):

        if hasattr(self, '_initialized') and self._initialized:
            return

        self.env, self.env_lower = self._get_env()
        self._venv_files = self._get_venv_files(relative_path)
        self._venv_files_encoding = 'utf-8'
        self._check_venv_files_exists()

        self.envs_params = environments_parameters.model_dump()
        self.env_params: TAccount = getattr(environments_parameters.accounts, self.env_lower)  # Fetching the current environment
        self.tags = Tags(_env_file=self._venv_files, _env_file_encoding=self._venv_files_encoding)
        self.cdk_env = Environment(account=self.env_params.id, region='eu-west-1')

        self.settings: TSettings = settings(_env_file=self._venv_files,
                                 _env_file_encoding=self._venv_files_encoding)  # Directly storing settings instance
        
        self.app_name = self.settings.app_name  # Accessing the app name from settings

        self._initialized = True

    @staticmethod
    def _get_env() -> (str, str):
        env = getenv("ENVIRONMENT", "Development")
        return env, env.lower()

    def _get_venv_files(self, relative_path: str) -> list[str]:
        dotenv_file = f'{relative_path}/.env.{self.env_lower}-iac'
        dotenv_file_local = f'{relative_path}/.env.{self.env_lower}-iac.private'

        env_files = []
        if path.isfile(dotenv_file):
            print(f'Using {dotenv_file}')
            env_files.append(dotenv_file)
        else:
            print(f'Not found {dotenv_file}')

        if not getenv("CI"):
            print(f'Local run. Trying to fetch private env file {dotenv_file_local}')
            if path.isfile(dotenv_file_local):
                env_files.append(dotenv_file_local)
            else:
                print(f'Not found {dotenv_file_local}')

        return env_files

    def _check_venv_files_exists(self) -> None:
        for file in self._venv_files:
            if not path.isfile(file):
                raise Exception(f'Expected venv file {file} does not exist')

    # app is not typed to avoid depending on aws cdk for this package
    def apply_tags(self, app):
        self.tags.mandatory.apply_tags(application=app, tag_list=self.tags.mandatory.model_dump())
