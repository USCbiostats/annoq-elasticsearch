import json
from setup_es import *

mapping = json.load(open("./data/vs_index_mapping.json"))
es.indices.put_mapping(index = 'annoq-test', body=mapping )
