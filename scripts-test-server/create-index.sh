host="http://localhost:9200"

curl -X PUT $host/annoq-annotations-v2 -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_replicas" : 0
  }
}
'