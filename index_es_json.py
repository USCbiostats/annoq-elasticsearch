import time
from elasticsearch import helpers, Elasticsearch
import ijson
import os
import sys
import pprint
from setup_es import es, ES_INDEX
#run python3 index_es_json test_input_json

def load_json(directory):
    
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            if name.endswith('.json'):
                print(os.path.join(root, name))
               # print("- %s seconds ---" % (time.time() - start_time))
                with open(os.path.join(root, name), 'r') as open_file:
                    parser = ijson.parse(open_file)
                    for value in ijson.items(parser, 'item'):
                        yield value

def bulk_load(directory):

    for success, info in helpers.parallel_bulk(es, load_json(directory), index=ES_INDEX, chunk_size=10000, request_timeout=200):
        if not success:
            print('A document failed:', info)

