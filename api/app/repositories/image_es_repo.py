from repositories.base_repo import BaseRepo
from cores.serach_engine.es import using_ES, must_and_must_not_query, aggressive_query, create_date_range_image, sort_query, match_field_analyzed
from cores.common import dump_str_to_date_format, viettnamese_regex_pattent
from schemas.es.image_es_schema import ES_FILE_INDEX, ES_FILE_SCHEMA


class ImageManager(BaseRepo):
    def __init__(self):
        super(ImageManager, self).__init__(ES_FILE_INDEX, ES_FILE_SCHEMA)

    @using_ES
    def search(self, is_search: bool = False, image_search_schemas: dict = {}, page: int = 1, page_size: int = 10):
        must = []
        must_not = []
        should = []
        aggs = {}
        for key, value in image_search_schemas.items():
            if value is not None:
                match_query = must_and_must_not_query(is_search=is_search, params={key: value})
                must += match_query.get('must', [])
                must_not += match_query.get('must_not', [])
                should += match_query.get('should', [])
        data = self.es.raw_search_query(start=page, size=page_size, must=must, must_not=must_not,should=should, aggs=aggs)
        return data

    @using_ES
    def insert_image(self, id: str, data):
        return self.es.insert(id=id, data=data)
    
    @using_ES
    def get_by_id(self, id: str):
        return self.es.get_by_id(id)

    @using_ES
    def update(self, id: str, data: dict()):
        return self.es.update(id, data)
    
    @using_ES
    def update_with_bulk(self, actions):
        return self.es.update_with_bulk(actions)
    
    @using_ES
    def delete(self, _id: str):
        return self.es.delete(_id)
