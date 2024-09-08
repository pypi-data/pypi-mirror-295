# Config provider for aws-cdk-constructs

## Usage

```python
from .environments_parameters import environments_parameters
from ..models.app_settings import AppSettings
from aws_cdk_constructs_config_provider import EnvironmentParameters, DefaultAccount, ConfigProvider

AppConfig = ConfigProvider[AppSettings, DefaultAccount]

envs = EnvironmentParameters[DefaultAccount].model_validate(environments_parameters)
appConfig = ConfigProvider[AppSettings, DefaultAccount](environments_parameters=envs, settings=AppSettings, relative_path='.')
```

## Development

any commit will trigger the semantic release versioning and changelog generation. Please follow the semantic release commit message format.