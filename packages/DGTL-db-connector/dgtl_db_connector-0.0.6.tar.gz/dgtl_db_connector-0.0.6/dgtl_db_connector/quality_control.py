from .client import Client
from .model import Model


class QualityControl(Model):
    table_name = "quality_control"
    primary_key = "uuid"
    auto_id = True
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.uuid: str|None = kwargs.get('uuid')
        self.metadata_pid: str = kwargs.get('metadata_pid')
        self.analyst_username: str = kwargs.get('analyst_username')
        self.grader_username: str = kwargs.get('grader_username')
        self.comments: str|None = kwargs.get('comments')
        self.feedback_items: list = self.convert_json(kwargs.get('feedback_items'))
