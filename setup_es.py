from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://bioghost2.usc.edu:9200'],
    port=9200,
    timeout=60
)

ES_INDEX = 'vs-index'
