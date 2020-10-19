host="http://bioghost2.usc.edu:9200"

curl -X PUT $host/vs-index -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 5,
    "number_of_replicas" : 0,
    "refresh_interval" : -1
  }
}
'

