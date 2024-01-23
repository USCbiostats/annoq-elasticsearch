import argparse
import load_env
from src.config.settings import settings
from src.config.es import es
from src.utils import load_json

class ElasticsearchIndexManager:
    def __init__(self, es_client, index_name, mappings, settings):
        self.es_client = es_client
        self.index_name = index_name
        self.mappings = mappings
        self.settings = settings

    def recreate_index(self):
        self.delete_index()
        self.create_index()
        self.put_mappings()

    def delete_index(self):
        self.es_client.options(ignore_status=[400, 404]).indices.delete(index=self.index_name)

    def create_index(self):
        self.es_client.options(ignore_status=[400]).indices.create(index=self.index_name, settings=self.settings)

    def put_mappings(self):
        self.es_client.indices.put_mapping(index=self.index_name, body=self.mappings)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Recreate Elasticsearch index with new settings and mappings.')
    parser.add_argument('--index_name', type=str, required=True, help='Name of the Elasticsearch index')
    parser.add_argument('--mappings_file', type=str, required=True, help='File path for index mappings')
    parser.add_argument('--settings_file', type=str, required=True, help='File path for index settings')
    return parser.parse_args()

def main():
    args = parse_arguments()

    annoq_mappings = load_json(args.mappings_file)
    annoq_settings = load_json(args.settings_file)

    index_manager = ElasticsearchIndexManager(es, args.index_name, annoq_mappings, annoq_settings)
    index_manager.recreate_index()

if __name__ == '__main__':
    main()
    
    
# python - src.reinit --index_name "your_index_name" --mappings_file "path/to/mappings.json" --settings_file "path/to/settings.json"
