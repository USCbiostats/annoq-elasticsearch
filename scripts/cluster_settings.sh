host="http://bioghost3.usc.edu:9200"

curl -XPUT -H "Content-Type: application/json" $host/_cluster/settings -d '
{ "persistent": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
curl -XPUT -H "Content-Type: application/json" $host/_all/_settings -d '
{"index.blocks.read_only_allow_delete": null}'

