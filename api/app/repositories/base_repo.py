from cores.serach_engine.es import Elasticsearch


class BaseRepo:
    # To use self.es call @using_ES before every function that about to use
    es: Elasticsearch = None

    def __init__(self, es_index: str, es_schema):
        self.es_index = es_index
        self.es_schema = es_schema
