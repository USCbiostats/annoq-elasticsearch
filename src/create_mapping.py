import json
from src.config.es import es

mapping = json.load(open("./data/annoq_mapping.json"))
es.indices.put_mapping(index = 'annoq-test', body=mapping )
