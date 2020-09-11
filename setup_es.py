from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['7fcc129ce17b4396b0a53c1e80dad9cf.us-west-1.aws.found.io'],
    http_auth=('elastic', 'skQu1NTHlkCmvEkLvcbCV1eI'),
    scheme="https",
    port=9243,
    timeout=60
)
