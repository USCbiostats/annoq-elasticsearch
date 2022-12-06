import json
from src.config.es import es

#delete old one
es.indices.delete(index='annoq-test', ignore=[400, 404])

es.options(ignore_status=[400, 404]).indices.delete(index=es_index)
es.options(ignore_status=[400]).indices.create(index=es_index, settings=add_settings())
#create and load mapping
es.indices.create(index='annoq-test', ignore=400)
mapping = json.load(open("./data/annoq_mapping.json"))
es.indices.put_mapping(index = 'annoq-test', body=mapping )
