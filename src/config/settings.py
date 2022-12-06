import os
from pydantic import BaseSettings

class Settings(BaseSettings):

    ANNOQ_ES_URL:str = os.environ.get("ANNOQ_ES_URL")
    ANNOQ_ES_PORT:str = os.environ.get("ANNOQ_ES_PORT")
    ANNOQ_ANNOTATIONS_INDEX :str = os.environ.get("ANNOQ_ANNOTATIONS_INDEX")
    PROJECT_TITLE: str = "Annoq"
    PROJECT_VERSION: str = "0.2.0"



settings = Settings()