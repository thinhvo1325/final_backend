from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from cores.serach_engine.es import using_ES, must_and_must_not_query, aggressive_query
from cores.serach_engine.es import Elasticsearch
es = Elasticsearch("image_manager_index")
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
import pandas as pd
from sklearn.decomposition import PCA
import hdbscan
for i in range(1, 1000):
    mmn = must_and_must_not_query(params={"user_id": i})
    result = es.raw_search_query(start=1, size=10000, must=mmn.get('must', []), must_not=mmn.get('must_not', []), should=mmn.get('should', []), aggs={})
    list_id = []
    list_embb = []
    if result.get('data') == []:
        continue
    for data in result.get('data'):
        for item in data.get("face_embedding"):
            list_id.append(data.get('_id'))
            list_embb.append(item.get('embedding'))
    df = pd.DataFrame({'list_id': list_id, 'embedding': list_embb})
    df = df[[ 'list_id',  'embedding']]
    embeddings = np.vstack(df['embedding'].to_numpy())
    ids = df['list_id'].to_list()

    pca = PCA(n_components=50)
    reduced_embeddings = pca.fit_transform(embeddings)

    hdbscan_clusterer = hdbscan.HDBSCAN(min_cluster_size=5)
    labels = hdbscan_clusterer.fit_predict(reduced_embeddings)
    df['cluster'] = labels
    for id, cluster, emmb in zip(ids, labels, embeddings):
        img = es.get_by_id(id)
        face_embedding = img.get('face_embedding')
        for item in face_embedding:
            if item.get('embedding') == emmb:
                item['cluster'] = cluster
        es.update(id, {"face_embedding": img.get('face_embedding')})



import time
time.sleep(86400*7)