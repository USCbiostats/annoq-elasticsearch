import json
from src.config.settings import settings
from src.config.es import es
from src.utils import load_json

#create and load mapping

if __name__=='__main__':
    annoq_mappings = load_json('./data/annoq_mapping.json')
    annoq_settings = load_json('./data/annoq_settings.json')
   
    #delete old one
    es.options(ignore_status=[400, 404]).indices.delete(index=settings.ANNOQ_ANNOTATIONS_INDEX)
    es.options(ignore_status=[400]).indices.create(index=settings.ANNOQ_ANNOTATIONS_INDEX, settings=annoq_settings) 
    es.indices.put_mapping(index = 'annoq-test', body=annoq_mappings)