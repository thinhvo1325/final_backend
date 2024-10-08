import functools
import math
import re
from unidecode import unidecode
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from elasticsearch import Elasticsearch as ES
from elasticsearch import helpers
from cores.common import DATE_FORMAT, DATETIME_FORMAT, SPLID_DATE_CHAR, FIELD_NOT_STR_FORMAT, viettnamese_regex_pattent
from decouple import config

class Elasticsearch:
    def __init__(self, index: str, init_config: dict = {}):
        self.index = index
        self.es = ES(f"http://103.69.97.62:9200")
        self.config_es(init_config)

    def close_es(self):
        self.es.close()

    @classmethod
    def get_all_indices(cls, start_with: str = '', contain: str = '', end_with: str = ''):
        self.es = ES(f"http://103.69.97.62:9200")
        data = es.indices.get_alias(index=f'{start_with}*{contain}*{end_with}').keys()
        es.close()
        return data

    def config_es(self, schema: dict):
        if not self.es.indices.exists(index=self.index):
            analyzer = {
                "tokenizer": "icu_tokenizer",
                "filter": ["icu_folding", "icu_normalizer"]
            }
            self.es.indices.create(index=self.index, body={
                "mappings": {
                    'properties': schema
                },
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "vi_analyzer": analyzer
                        }
                    },
                    "index": {
                        "blocks": {
                            "read_only_allow_delete": None,
                            "write": False
                        }
                    }
                }
            })

    def get_index(self):
        """
        Retrieves the index information.

        Returns:
            dict: The index information.
        """
        return self.es.indices.get_alias(index="*")

    def get_mapping(self, index: str):
        """
        Retrieves the mapping and settings of a specific index.

        Args:
            index (str): The name of the index.

        Returns:
            dict: The mapping and settings of the index.
        """
        return {'mapping': self.es.indices.get_mapping(index=index), 'setting': self.es.indices.get_settings(index=index)}
    
    def update_by_query(self, index: str, scripts: str, query: str):
        """
        Updates documents in the index using a query.

        Args:
            index (str): The name of the index.
            scripts (str): The update scripts.
            query (str): The query to filter the documents.

        Returns:
            dict: The response from Elasticsearch.
        """
        return self.es.update_by_query(index=index, script=scripts, query=query)
    
    def delete_by_query_config(self, index: str, query: dict):
        """
        Deletes documents in the index using a query.

        Args:
            index (str): The name of the index.
            query (dict): The query to filter the documents.

        Returns:
            dict: The response from Elasticsearch.
        """
        return self.es.delete_by_query(index=index, query=query)
    
    def update_mapping(self, field):
        """
        Updates the mapping of the index.

        Args:
            field: The field to be updated.

        Returns:
            dict: The response from Elasticsearch.
        """
        self.es.indices.put_mapping(index=self.index, properties=field)

    def refresh(self):
        """
        Refreshes the index.
        """
        self.es.indices.refresh(index=self.index)

    def create_index(self, index: str, schema: dict):
        """
        Creates a new index with the specified schema.

        Args:
            index (str): The name of the index.
            schema (dict): The schema of the index.
        """
        analyzer = {
                "tokenizer": "icu_tokenizer",
                "filter": ["icu_folding", "icu_normalizer"]
            }
        self.es.indices.create(index=index, body={
            "mappings": {
                'properties': schema
            },
            "settings": {
                "analysis": {
                    "analyzer": {
                        "vi_analyzer": analyzer
                    }
                },
                "index": {
                    "blocks": {
                        "read_only_allow_delete": None,
                        "write": False
                    }
                }
            }
        })


    def delete_index(self, index: str):
        """
        Deletes the specified index.

        Args:
            index (str): The name of the index.
        """
        self.es.indices.delete(index=index)

    def re_index(self, source: str, des: str):
        """
        Reindexes documents from one index to another.

        Args:
            source (str): The source index.
            des (str): The destination index.
        """
        self.es.reindex(source={"index": source}, dest={"index": des})

    def update_setting(self):
        """
        Updates the settings of the index.
        """
        self.es.indices.put_settings(
            index=self.index,
            body={
                "settings": {
                    "index": {
                        "blocks": {
                            "read_only_allow_delete": None
                        }
                    }
                }
            }
        )

    def insert(self, data: dict() = {}, id: str = None):
        """
        Inserts a new document into the index.

        Args:
            data (dict): The data to be inserted.
            id (str): The ID of the document.

        Returns:
            dict: The response from Elasticsearch.
        """
        for key, value in data.items():
            if isinstance(value, datetime):
                data.update({key: value.strftime(DATETIME_FORMAT)})
            elif isinstance(value, date):
                data.update({key: value.strftime(DATE_FORMAT)})

        self.update_setting()
        return self.es.index(
            index=self.index,
            body=data,
            id=id,
            refresh=True
        )

    def update(self, id: str, update_data: dict):
        """
        Updates an existing document in the index.

        Args:
            id (str): The ID of the document.
            update_data (dict): The data to be updated.

        Returns:
            dict: The response from Elasticsearch.
        """
        self.update_setting()
        for key, value in update_data.items():
            if isinstance(value, datetime):
                update_data.update({key: value.strftime(DATETIME_FORMAT)})
            elif isinstance(value, date):
                update_data.update({key: value.strftime(DATE_FORMAT)})
        return self.es.update(
            index=self.index,
            id=id,
            body={
                'doc': update_data
            },
            refresh=True
        )

    def update_with_bulk(self, actions):
        """
        Updates multiple documents in the index using bulk API.

        Args:
            actions: The actions to be performed.

        Returns:
            dict: The response from Elasticsearch.
        """
        self.update_setting()
        helpers.bulk(self.es, actions=actions)


    def delete(self, id: str):
        """
        Deletes a document from the index.

        Args:
            id (str): The ID of the document.

        Returns:
            dict: The response from Elasticsearch.
        """
        self.update_setting()
        return self.es.delete(
            index=self.index,
            id=id,
            refresh=True
        )

    def delete_by_query(self, params: dict = {}, nested_params: dict = {}):
        """
        Deletes documents from the index using a query.

        Args:
            params (dict): The parameters for the query.
            nested_params (dict): The nested parameters for the query.
        """
        query = self.__get_query_params__(params, nested_params)
        self.update_setting()
        self.es.delete_by_query(
            index=self.index,
            body={'query': query},
            refresh=True
        )
    
    def raw_search(self, search_body):
        """
        Performs a raw search query on the index.

        Args:
            start (int): The starting page of the search results.
            size (int): The number of results per page.
            must (list): The list of must conditions.
            must_not (list): The list of must not conditions.
            should (list): The list of should conditions.
            aggs (dict): The aggregations to be performed.
            sort (any): The sorting criteria.

        Returns:
            dict: The search results.
        """
    
        response = self.es.search(
            index=self.index,
            body=search_body
        )
        return response
    def raw_search_query(self, start: int = 1, size: int = 10, must: list = [], must_not: list = [], should: list = [],
                         aggs: dict = {}, sort: any = {}):
        """
        Performs a raw search query on the index.

        Args:
            start (int): The starting page of the search results.
            size (int): The number of results per page.
            must (list): The list of must conditions.
            must_not (list): The list of must not conditions.
            should (list): The list of should conditions.
            aggs (dict): The aggregations to be performed.
            sort (any): The sorting criteria.

        Returns:
            dict: The search results.
        """
        print({
                'from': (start-1) * size,
                'size': size,
                'query': {"bool": {"must": must, "must_not": must_not, "should": should}},
                'sort': sort,
                'aggs': aggs
            })
        response = self.es.search(
            index=self.index,
            body={
                'from': (start-1) * size,
                'size': size,
                'query': {"bool": {"must": must, "must_not": must_not, "should": should}},
                'sort': sort,
                'aggs': aggs
            }
        )
        info = response.get('hits')
        total = info.get('total').get('value')
        data = info.get('hits')
        aggregation = response.get('aggregations')

        total_page = math.ceil(total/size) if size > 0 else 0
        reutrn_data = []
        
        for item in data:
            _source = item.get('_source')
            _source.update({'_id': item.get('_id')})
            reutrn_data.append(_source)
        return {
            'data': reutrn_data,
            'aggregation': aggregation,
            'page': start,
            'size': size,
            'total_data': total,
            'total_page': total_page
        }

    def get_by_id(self, id: str):
        """
        Retrieves a document from the index by its ID.

        Args:
            id (str): The ID of the document.

        Returns:
            dict: The document.
        """
        try:
            response = self.es.get(index=self.index, id=id)
        except Exception:
            return None
        return response.get('_source', None)


# Must be call as @decorator before every function that use elasticsearch
def using_ES(func):
    """
    A decorator that should be called before every function that uses Elasticsearch.

    Args:
        func: The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.es_index and not self.es_schema:
            raise NotImplementedError('Must be config es_index and es_schema as class attribute before use')
        self.es = Elasticsearch(self.es_index, self.es_schema)
        result = func(self, *args, **kwargs)
        self.es.close_es()
        return result

    return wrapper


def create_date_filter(format_date: str, process_date: date = None,
                       year_delta: int = 1, month_delta: int = 1, day_delta: int = 1):
    """
    Creates a date filter for Elasticsearch queries.

    Args:
        format_date (str): The format of the date.
        process_date (date): The date to be processed.
        year_delta (int): The number of years to add to the process date.
        month_delta (int): The number of months to add to the process date.
        day_delta (int): The number of days to add to the process date.

    Returns:
        dict: The date filter.
    """
    interval = 'year'
    format = 'yyyy'
    range_filter = {}

    if format_date == '%Y':
        range_filter = {
            "format": format,
            "gte": process_date.strftime(format_date),
            "lt": (process_date + relativedelta(years=year_delta)).strftime(format_date)
        }
        interval = 'day'
        format += '/MM/dd'
    elif format_date == SPLID_DATE_CHAR.join(['%Y', '%m']):
        format += '/MM'
        range_filter = {
            "format": format,
            "gte": process_date.strftime(format_date),
            "lt": (process_date + relativedelta(months=month_delta)).strftime(format_date)
        }
        interval = 'day'
        format += '/dd'

    elif format_date == DATE_FORMAT:
        format += '/MM/dd'
        range_filter = {
            "format": format,
            "gte": process_date.strftime(format_date),
            "lt": (process_date + relativedelta(days=day_delta)).strftime(format_date)
        }

    return {"interval": interval, "format": format, "range_filter": range_filter}

def create_date_range_image(format_date: str, start_date: date = None, end_date: date = None):
    """
    Creates a date range filter for Elasticsearch queries on image_info field.

    Args:
        format_date (str): The format of the date.
        start_date (date): The start date of the range.
        end_date (date): The end date of the range.

    Returns:
        dict: The date range filter.
    """
    range_filter = {'nested': {
                        'path': 'image_info', 
                        'query': {
                            'bool': {
                                'must': [{
                                    'range': {
                                        'image_info.captured_date': {
                                            'format': 'yyyy/MM/dd HH:mm:ss', 
                                            'gte': start_date.strftime(format_date) + ' 00:00:00', 
                                            'lt': end_date.strftime(format_date)+  ' 23:59:59'}
                                        }
                                    }]                     
                                }
                            }
                        }
                    }
    return range_filter

def range_time_event(format_date: str, start_date: date = None, end_date: date = None):
    """
    Creates a range filter for Elasticsearch queries on start_date field.

    Args:
        format_date (str): The format of the date.
        start_date (date): The start date of the range.
        end_date (date): The end date of the range.

    Returns:
        dict: The range filter.
    """
    range_filter =  [{
                        'range': {
                            'start_date': {
                                'format': 'yyyy/MM/dd HH:mm:ss', 
                                'gte': start_date.strftime(format_date) + ' 00:00:00',
                                'lte': end_date.strftime(format_date)+  ' 23:59:59'}
                            }
                        },
                        {
                        'range': {
                            'end_date': {  
                                'format': 'yyyy/MM/dd HH:mm:ss', 
                                'gte': start_date.strftime(format_date) + ' 00:00:00', 
                                'lte': end_date.strftime(format_date)+  ' 23:59:59'}
                            }
                        },
                        {
                            "bool": {
                                "must": [
                                    {
                                    'range': {
                                        'start_date': {  
                                            'format': 'yyyy/MM/dd HH:mm:ss', 
                                            'lte': start_date.strftime(format_date) + ' 00:00:00'}
                                        }
                                    },
                                    {
                                    'range': {
                                        'end_date': {  
                                            'format': 'yyyy/MM/dd HH:mm:ss', 
                                            'gte': end_date.strftime(format_date)+  ' 23:59:59'}
                                        }
                                    },
                                ]
                            }
                        }
                        # {
                        #     "bool": {
                        #         "must": [
                        #             {
                        #             'range': {
                        #                 'end_date': {  
                        #                     'format': 'yyyy/MM/dd HH:mm:ss', 
                        #                     'gte': start_date.strftime(format_date) + ' 00:00:00'}
                        #                 }
                        #             },
                        #             {
                        #             'range': {
                        #                 'end_date': {  
                        #                     'format': 'yyyy/MM/dd HH:mm:ss', 
                        #                     'gte': end_date.strftime(format_date)+  ' 23:59:59'}
                        #                 }
                        #             },
                        #         ]
                        #     }
                        # }]
    ]                     

    return range_filter

def match_field_analyzed(type_match_field: str = "must", type_match_in_nested: str = "must", parents: list = [], params: dict = {}):
    query = {
        "must": [],
        "must_not": [],
        "should": []
    }
    
    for field, value in params.items():
        if len(parents)>0:
            field = f'{parents[0]}.{field}'
        if len(value.split(' '))==1:
            if re.search(viettnamese_regex_pattent, value):
                query.get(type_match_field).append({"wildcard": {f'{field}.keyword': f'*{value}*'}})
                query.get(type_match_field).append({"wildcard": {f'{field}': f'*{value}*'}})
            else:
                query.get(type_match_field).append({"wildcard": {f'{field}.analyzed': f'*{value}*'}})
                if ('-' in value) or ('(' in value) or (')' in value):
                    query.get(type_match_field).append({"wildcard": {f'{field}': f'*{value}*'}})
                    query.get(type_match_field).append({"wildcard": {f'{field}.keyword': f'*{value}*'}})
        else:
            if re.search(viettnamese_regex_pattent, value):
                query.get(type_match_field).append({
                                                    "match_phrase": {
                                                        f"{field}": {
                                                            "query": f'*{value}*',
                                                            # "analyzer": "vi_analyzer"
                                                            }
                                                        },
                                                    })
            else:
                query.get(type_match_field).append({
                                                    "match_phrase": {
                                                        f"{field}.analyzed": {
                                                            "query": f'*{value}*',
                                                            "analyzer": "vi_analyzer"
                                                            }
                                                        },
                                                    })
    
    for item in list(reversed(parents)):
        nested_parents_query = {
            'nested': {
                "path": item,
                "query": {
                    'bool': {
                        'must': query.get("must"),
                        'must_not': query.get("must_not"),
                        'should': query.get("should")
                    }
                }
            }
        }
        
        return {
            type_match_in_nested: [nested_parents_query]
        }

    return query

               

def must_and_must_not_query(is_search: bool = False, parents: list = [], params: dict = {}, not_params: dict = {},
                            extra_params: list[dict] = None, not_extra_params: list[dict] = None):

    must = []
    must_not = []
    should_nested = []
    should = []
    parent_prefix = ''

    for item in parents:
        parent_prefix += f'{item}.'

    for key, value in params.items():
        if value is not None:
            if key == 'checking_item_exists':
                must.append({"exists": {'field': f'{parent_prefix}{value}'}})
            elif isinstance(value, dict):
                date_filter = create_date_filter(process_date=value.get('value'),
                                                      format_date=value.get('format'))
                must.append({"range": {f'{parent_prefix}{key}': date_filter.get('range_filter')}})
            else:
                if not is_search:
                    must.append({"match": {f'{parent_prefix}{key}': value}})
                else:
                    if key in ['object_id']:
                        must.append({"match": {f'object_list.class': value}})
                    elif key in ['text_list']:
                        should_in_must = []
                        value = unidecode(value.strip().lower())
                        if len(value.split(' '))==1:
                            if re.search(viettnamese_regex_pattent, value):
                                should_in_must.append({"wildcard": {f'{parent_prefix}{key}.keyword': f'*{value}*'}})
                                should_in_must.append({"wildcard": {f'{parent_prefix}{key}': f'*{value}*'}})
                            else:
                                should_in_must.append({"wildcard": {f'{parent_prefix}{key}.analyzed': f'*{value}*'}})
                                if ('-' in value) or ('(' in value) or (')' in value):
                                    should_in_must.append({"wildcard": {f'{parent_prefix}{key}.keyword': f'*{value}*'}})
                                    should_in_must.append({"wildcard": {f'{parent_prefix}{key}': f'*{value}*'}})
                        else:
                            if re.search(viettnamese_regex_pattent, value):
                                    should_in_must.append({
                                                    "match_phrase": {
                                                        f"{parent_prefix}{key}": {
                                                            "query": f'*{value}*'},
                                                            # "analyzer": "vi_analyzer"
                                                        }
                                                    })
                            else:
                                should_in_must.append({
                                                "match_phrase": {
                                                    f"{parent_prefix}{key}.analyzed": {
                                                        "query": f'*{value}*'},
                                                        # "analyzer": "vi_analyzer"
                                                    }
                                                })
                        must.append({'bool': {'should': should_in_must}})
                    
    for key, value in not_params.items():
        if value is not None:
            if key == 'checking_item_exists':
                must_not.append({"exists": {'field': f'{parent_prefix}{value}'}})
            elif isinstance(value, dict):
                date_filter = create_date_filter(process_date=value.get('value'),
                                                 format_date=value.get('format'))
                must_not.append({"range": {f'{parent_prefix}{key}': date_filter.get('range_filter')}})
            elif isinstance(value, list):
                for item in value:
                    must_not.append({"match": {f'{parent_prefix}{key}': item}})
            else:
                must_not.append({"match": {f'{parent_prefix}{key}': value}})
    for item in list(reversed(parents)):
        nested_parents_query = {
            'nested': {
                "path": item,
                "query": {
                    'bool': {
                        'must': must,
                        'must_not': must_not,
                        'should': should_nested
                    }
                }
            }
        }
        must = [nested_parents_query]
        must_not = []

    if extra_params is not None:
        for item in extra_params:
            if len(item) > 0:
                for key, value in item.items():
                    if key in ['must', 'must_not', 'should']:
                        must.append({
                            'bool': {key: value}
                        })
    if not_extra_params is not None:
        for item in extra_params:
            if len(item) > 0:
                for key, value in item.items():
                    if key in ['must', 'must_not', 'should']:
                        must_not.append({
                            'bool': {key: value}
                        })

    return {
        'must': must,
        'must_not': must_not,
        'should': should
    }


def should_query(parents: list = [], params: dict = {}, extra_params: list[dict] = None,
                 not_extra_params: list[dict] = None):
    should = []
    parent_prefix = ''
    for item in parents:
        parent_prefix += f'{item}.'

    for key, value in params.items():
        if value is not None:
            if key == 'checking_item_exists':
                should.append({"exists": {'field': f'{parent_prefix}{value}'}})
            elif isinstance(value, dict):
                date_filter = create_date_filter(process_date=value.get('value'),
                                                      format_date=value.get('format'))
                should.append({"range": {f'{parent_prefix}{key}': date_filter.get('range_filter')}})
            else:
                should.append({"match": {f'{parent_prefix}{key}': value}})

    for item in list(reversed(parents)):
        nested_parents_query = {
            'nested': {
                "path": item,
                "query": {
                    'bool': {
                        'should': should,
                    }
                }
            }
        }
        should = [nested_parents_query]

    if extra_params is not None:
        for item in extra_params:
            if len(item) > 0:
                for key, value in item.items():
                    if key in ['must', 'must_not', 'should']:
                        should.append({
                            'bool': {key: value}
                        })
    return {
        'should': should,
    }


def aggressive_query(parents: list = [], params: dict = {}):
    aggs = {}
    parent_prefix = ''
    for item in parents:
        parent_prefix += f'{item}.'
    for key, value in params.items():
        if value is not None:
            if isinstance(value, dict):
                date_filter = create_date_filter(process_date=value.get('value'), format_date=value.get('format'))
                aggs[key] = {
                    "date_histogram": {
                        "field": f'{parent_prefix}{key}',
                        "interval": date_filter.get("interval"),
                        "format": date_filter.get("format"),
                        "min_doc_count": 1
                    }
                }
        else:
            aggs[key] = {
                "terms": {
                    "field": f'{parent_prefix}{key}'
                }
            }
    for item in list(reversed(parents)):
        aggs = {
            item: {
                'nested': {
                    'path': parent_prefix[:-1]
                },
                'aggs': aggs
            }
        }
        parent_prefix = parent_prefix.replace(f'{item}.', '')

    return aggs

def sort_query(parent: str = None, sort_by: str = None, order: str = None):
    sort = {}
    if sort_by == '_score':
        return {sort_by : {'order': order}} 
    
    if sort_by is None and order is None:
        return sort

    if sort_by not in FIELD_NOT_STR_FORMAT:
        sort_by = f'{sort_by}.keyword'
    
    if parent is None:
        sort[sort_by] = {'order': order}
    else:
        sort[f'{parent}.{sort_by}'] = {
            'order': order,
            'nested': {
                'path': parent
            }
        }
    return sort
