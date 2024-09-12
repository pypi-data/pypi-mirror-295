import json
from datetime import datetime
from uuid import uuid4


class Model:
    def __init__(self):
        if not hasattr(self, 'table_name'):
            raise ValueError("You must define a table name for the model")
        if not hasattr(self, 'primary_key'):
            raise ValueError("You must define a primary key for the model")
        if not hasattr(self, 'client'):
            raise ValueError("You must define a client for the model")
        if(not hasattr(self, 'auto_id')):
            self.auto_id = True
    
    def __format_data(self):
        data = {}
        for k, v in self.__dict__.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
            if(isinstance(v, list)):
                data[k] = json.dumps(v)
            else:
                data[k] = v
        return data

    def create(self):
        data = self.__format_data()
        if self.auto_id:
            data[self.primary_key] = str(uuid4())
        data['created_at'] = datetime.utcnow().isoformat()
        self.client.add_entry(data)
    
    def update(self):
        data = self.__format_data()
        id = data[self.primary_key]
        data['updated_at'] = datetime.utcnow().isoformat()
        self.client.modify_entry(data=data, index=(self.primary_key, id))

    def delete(self):
        self.client.remove_entry(data=(self.primary_key, self.__dict__[self.primary_key]))

    def convert_datetime(self, iso_str):
        if(type(iso_str) == datetime):
            return iso_str
        if(iso_str == None):
            return None
        return datetime.fromisoformat(iso_str)
    
    def convert_json(self, json_str):
        if(type(json_str) == list):
            return json_str
        if(json_str == None):
            return None
        return json.loads(json_str)

    @classmethod
    def set_table_name(cls, name):
        cls.table_name = name

    @classmethod
    def set_primary_key(cls, key):
        cls.primary_key = key

    @classmethod
    def find(cls, id, columns: list|None=None):
        columns_string = None
        if columns is not None:
            columns_string = ", ".join(columns)
        data = cls.client.read_entry(indices=[(cls.primary_key, id)], column=columns_string or "*")
        if len(data) == 0:
            return None
        else:
            instance = cls(**data[0])
            return instance
        
    @classmethod
    def where(cls, index: str, value: str):
        if not hasattr(cls, "_query"):
            cls._query = []
        cls._query.append(("AND", index, value))
        return cls
    
    @classmethod
    def or_where(cls, index: str, value: str):
        if not hasattr(cls, "_query"):
            cls._query = []
        cls._query.append(("OR", index, value))
        return cls
    
    @classmethod
    def where_in(cls, index: str, values: list):
        first = True
        if not hasattr(cls, "_query"):
            cls._query = []
        for value in values:
            if first:
                cls._query.append(("AND", index, value))
                first = False
            else:
                cls._query.append(("OR", index, value))
        return cls
    
    @classmethod
    def or_where_in(cls, index: str, values: list):
        if not hasattr(cls, "_query"):
            cls._query = []
        for value in values:
            cls._query.append(("OR", index, value))
        return cls
    
    @classmethod
    def get(cls, page=1, page_size=10, columns: list|None=None):
        columns_string = ", ".join(columns) if columns is not None else "*"
        if not hasattr(cls, "_query"):
            cls._query = []
        data = cls.client.read_entry(conditions=cls._query, column=columns_string, page=page, page_size=page_size)
        del cls._query
        return [cls(**d) for d in data]
        
