from dependency_injector import containers, providers
from src.infrastructure.db.mongo_client import MongoDBClient
from src.core.repositories.db_repository import DBRepository
from src.infrastructure.pika import PikaClient
from src.infrastructure.db.redis_client import RedisClient
from src.core.repositories.rabbitmq_repository import RabbitMQRepository
from src.services.gateway_service import GatewayService
from src.services.ms_service import MicroserviceService
from src.core.use_cases.rabbitmq.consume_user_auth_queue import ConsumeUserAuthQueue

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for the Gateway Service."""
    
    config = providers.Configuration()

    # MongoDB Client (Singleton)
    mongo_client = providers.Singleton(
        MongoDBClient,
        db_uri=config.db_uri,
        db_name=config.db_name,
        db_collection=config.db_collection
    )

    # Redis Client (Singleton using the new RedisClient class)
    redis_client = providers.Singleton(
        RedisClient,
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db,
        password=config.redis_password
    )

    # RabbitMQ Client (Singleton)
    rabbitmq_client = providers.Singleton(
        PikaClient,
        rabbitmq_host=config.rabbitmq_host
    )

    db_repository = providers.Factory(
        DBRepository,
        client=mongo_client
    )

    rabbitmq_repository = providers.Factory(
        RabbitMQRepository,
        pika_client=rabbitmq_client
    )

    # Gateway Service (Singleton)
    gateway_service = providers.Factory(
        GatewayService,
        mongo_client=mongo_client,
        redis_client=redis_client
    )

    # MicroserviceRegistrationService Factory with dependencies
    microservice_service = providers.Factory(
        MicroserviceService,
        db_repository=db_repository
    )

    # Consume User Auth Queue use case
    consume_user_auth_queue = providers.Factory(
        ConsumeUserAuthQueue,
        repository=rabbitmq_repository
    )
