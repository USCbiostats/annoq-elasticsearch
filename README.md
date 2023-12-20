# annoq data admin

Scripts for load data and Elasticsearch mapping of AnnoQ

## Dependents on two data files

* ./data/doc_type.pkl
* ./data/annoq_mapping.json

## Converting and Indexing Elasticsearch

### Converting

1. install packages in requirement.txt
2. convert the resulting wgsa_add PANTHER and ENHANCER vcf or tsc files to json
3. use run_jobs.sh for production and run_job local for local setup

### Indexing 
1. run `sh scripts-test-server/create_index.sh` to create index.
2. run `python3 create_mapping.py` to load mapping
3. run `python index_es_json.py` to load into elasticsearch
