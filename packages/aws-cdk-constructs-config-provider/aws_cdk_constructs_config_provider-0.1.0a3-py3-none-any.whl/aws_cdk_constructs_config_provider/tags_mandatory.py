from typing import Dict

from aws_cdk import Tags, App
from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class FaoTagsStrategy(BaseSettings):
    """
    All mandatory tags by the Cloud Team
    """
    model_config = SettingsConfigDict(extra='ignore')
    ApplicationName: str = Field(..., alias="application_name")
    Environment: str = Field(..., alias="environment")
    BusinessOwner1: str = Field(default=None, alias="business_owner")
    BudgetCode1: str = Field(default=None, alias="budget_code")
    BudgetHolder1: str = Field(default=None, alias="budget_holder")

    @staticmethod
    def apply_tags(application: App, tag_list: Dict) -> None:
        for tag, value in tag_list.items():
            if value:
                Tags.of(application).add(
                    tag,
                    value,
                    apply_to_launched_instances=True,
                )
