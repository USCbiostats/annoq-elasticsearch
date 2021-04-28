from elasticsearch import Elasticsearch
from elasticsearch import helpers
import fileinput
import pickle
import json
from setup_es import *

#delete old one
es.indices.delete(index='annoq-test', ignore=[400, 404])
#create and load mapping
es.indices.create(index='annoq-test', ignore=400)
mapping = json.load(open("./data/vs_index_mapping.json"))
es.indices.put_mapping(index = 'annoq-test', body=mapping )
