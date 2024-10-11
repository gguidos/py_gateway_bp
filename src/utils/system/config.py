# src/config.py
from dotenv import load_dotenv

load_dotenv()

def load_config(container):
    container.config.db_uri.from_env("MONGO_URI")
    container.config.db_name.from_env("DB_NAME")
    container.config.db_collection.from_env("DB_COLLECTION")
    container.config.redis_host.from_env("REDIS_HOST", default="localhost")
    container.config.redis_port.from_env("REDIS_PORT", default=6379)
    container.config.redis_db.from_env("REDIS_DB", default=0)
    container.config.redis_password.from_env("REDIS_PASSWORD", default=None)
    container.config.rabbitmq_host.from_env("RABBITMQ_HOST")
