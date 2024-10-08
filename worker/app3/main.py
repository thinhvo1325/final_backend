from cores.serach_engine.es import Elasticsearch, must_and_must_not_query
import numpy as np
import hdbscan
from services.user_service import UserService

es = Elasticsearch("image_manager_index")

for i in range(1, 1000):
    must = must_and_must_not_query(params={"user_id": i})
    images = es.raw_search_query(must=must.get("must"), size=10000)
    if images['data'] == []:
        break
    list_embedded = []
    list_id = []
    for item in images['data']:
        if item['face_embedding'] != ([0.0] * 512):
            list_id.append(item['_id'])
            list_embedded.append(item['face_embedding'])
    embedding_matrix = np.vstack(list_embedded)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=3)
    cluster_labels = clusterer.fit_predict(embedding_matrix)
    for image_id, cluster in zip(list_id, cluster_labels):
        es.update(image_id, {"cluster": cluster})

# To run the async function


# r = es.get_by_id('7f3d9b2d-d06c-4fb8-8de7-2c2c6e06ea11')
# print(r['face_embedding'] == ([0.0] * 512))