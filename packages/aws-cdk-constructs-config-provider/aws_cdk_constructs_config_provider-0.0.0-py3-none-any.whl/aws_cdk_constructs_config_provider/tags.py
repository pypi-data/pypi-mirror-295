from .tags_mandatory import FaoTagsStrategy
from .tags_scheduler import TagScheduler


class Tags:
    def __init__(self, **kwargs):
        self.mandatory = FaoTagsStrategy(**kwargs)
        self.scheduler = TagScheduler(**kwargs)
