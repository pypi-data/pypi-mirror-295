from pydantic_settings import BaseSettings, SettingsConfigDict


class TagScheduler(BaseSettings):
    """
    Class to aggregate all Scheduler configuration tags
    """
    model_config = SettingsConfigDict(extra='ignore', env_prefix='tag_scheduler_')
    uptime: str = "08:00-18:00"
    uptime_days: str = "1-2-3-4-5"
    uptime_skip: str = "false"
