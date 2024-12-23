from cores.common import ES_DATE_FORMAT

ES_FILE_INDEX = "image_manager_index"
ES_FILE_SCHEMA = {
    "image_id": {
        "type": "text",
        "fields": {
            "keyword": {
                "type": "keyword"
            }
        }
    },
    "resource_path": {
        "type": "text",
        "fields": {
            "keyword": {
                "type": "keyword"
            }
        }
    },
    "is_public": {
        "type": "boolean"
    },
    "user_id": {
        "type": "integer"
    },
    "created_date": {
        "type": "date",
        "format": "yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||yyyy/MM||yyyy"
    },
    "face_embedding": {
        "properties": {
            # "facial_area": {
            #     "type": "text",
            #     "fields": {
            #         "keyword": {
            #             "type": "keyword",
            #             "ignore_above": 256
            #         },
            #         "analyzed": {
            #             "type": "text",
            #             "analyzer": "vi_analyzer"
            #         }
            #     }
            # },
            "embedding": {
                "type": "float"
            },
            "cluster": {
                "type": "integer"
            }
        }
    },
    "text_list": {
        "type": "text",
        "fields": {
            "keyword": {
                "type": "keyword"
            },
            "analyzed": {
                "type": "text",
                "analyzer": "vi_analyzer"
            }
        }
    },
    "object_list": {
        "properties": {
            "object_name": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    },
                    "analyzed": {
                        "type": "text",
                        "analyzer": "vi_analyzer"
                    }
                }
            },
            "object_id": {
                "type": "long"
            },
            "object_score": {
                "type": "float"
            },
            "object_box": {
                "type": "float"
            }
        }
    }
}

