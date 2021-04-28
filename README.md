# annoq data admin

Scripts for load data and Elasticsearch mapping of AnnoQ

## Dependents on two data files

* ./data/doc_type.pkl
* ./data/vs_index_mapping.json

## Running 

1. install packages in requirment.txt
2. make ES settings in `setup_es.py` and `create_index.sh`
3. run `sh create_index.sh` to create index
4. run `python3 reinit.py` to load mapping
5. set data dir in import.sh and run `sh import.sh`
