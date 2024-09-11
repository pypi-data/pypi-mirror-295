from client import Client
from model import Model


class QualityControlFeedback(Model):
    table_name = "qc_feedback"
    primary_key = "uuid"
    auto_id = True
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.uuid: str|None = kwargs.get('uuid')
        self.qc_uuid: str = kwargs.get('qc_uuid')
        self.penalty: str = kwargs.get('penalty')
        self.description: str = kwargs.get('description')
