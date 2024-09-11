class Model:
    def __init__(self):
        if not hasattr(self, 'table_name'):
            raise ValueError("You must define a table name for the model")
        if not hasattr(self, 'primary_key'):
            raise ValueError("You must define a primary key for the model")
        if not hasattr(self, 'client'):
            raise ValueError("You must define a client for the model")

    def create(self):
        data = {k: v for k, v in self.__dict__.items()}
        self.client.add_entry(data)
    
    def update(self):
        data = {k: v for k, v in self.__dict__.items()}
        id = data[self.primary_key]
        self.client.modify_entry(data=data, index=(self.primary_key, id))

    def delete(self):
        self.client.remove_entry(data=(self.primary_key, self.__dict__[self.primary_key]))

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
        data = cls.client.read_entry((cls.primary_key, id), column=columns_string or "*") 
        if len(data) == 0:
            return None
        else:
            instance = cls(**data[0])
            return instance
    
    @classmethod
    def where(cls, index: str, value: str):
        if not hasattr(cls, "_query"):
            cls._query = []
        cls._query.append((index, value))
        return cls

    @classmethod
    def get(cls, page=1, page_size=10, columns: list|None=None):
        columns_string = ", ".join(columns) if columns is not None else "*"
        if not hasattr(cls, "_query"):
            cls._query = []
        data = cls.client.read_entry(indices=cls._query, column=columns_string, page=page, page_size=page_size)
        del cls._query
        if(int(data.get('ResponseMetadata').get('HTTPStatusCode')) == 200):
            return IndexResponse(data=[cls(**d) for d in data['Items']], success=True, count=data['Count'])
        else:
            return IndexResponse(data=[], success=False, count=0)
        

class IndexResponse():
    def __init__(self, data: list, success: bool, count: int):
        self.success = success
        self.data = data
        self.count = count