from elasticsearch import Elasticsearch
from src.config.settings import settings


es = Elasticsearch(settings.ANNOQ_ES_URL, port=settings.ANNOQ_ES_PORT,    timeout=60)