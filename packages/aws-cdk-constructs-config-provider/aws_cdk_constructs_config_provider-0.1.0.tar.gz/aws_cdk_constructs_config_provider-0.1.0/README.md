# Config provider for aws-cdk-constructs

## Usage

```python
from .environments_parameters import environments_parameters
from ..models.app_settings import AppSettings
from aws_cdk_constructs_config_provider import DefaultAccount, ConfigProvider

appConfig = ConfigProvider[AppSettings, DefaultAccount](environments_parameters=environments_parameters, settings=AppSettings, relative_path='.')
```

## Development

**Please follow the semantic release commit message format.**

### Branches

#### develop
The `develop` branhces is the main branch for development. All feature branches should be created from this branch any commit to the development branch will create an `alpha` version.

#### feature/*
The `feature/*` branches are the branches for new features. Any commit to a feature branch will create a `beta` version.

#### main
The `main` branch is the production branch. Any commit to the main branch will create a `release` version.