# src/lifespan.py
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from src.utils.dynamic_router import register_microservice_routes
import logging
from threading import Thread
import json

logger = logging.getLogger(__name__)

def start_rabbitmq_consumer(container):
    """Function to start consuming from RabbitMQ user authentication queue"""
    consume_user_auth_queue = container.consume_user_auth_queue()

    def on_user_auth_message(ch, method, properties, body):
        # Process the message received from the RabbitMQ queue
        user_data = json.loads(body)
        logger.info(f"Processing authentication for user: {user_data.get('user_wallet_address')}")
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Start consuming messages from the queue
    consume_user_auth_queue.execute(on_user_auth_message)


@asynccontextmanager
async def lifespan(app):
    """Lifespan event manager to handle startup and shutdown events."""
    container = app.container

    try:
        mongo_client = container.mongo_client()
        await mongo_client.connect()
        redis_client = container.redis_client()
        await redis_client.connect()
        logger.info("MongoDB and Redis clients connected during startup.")

        microservice_service = container.microservice_service()
        microservices = await microservice_service.get_all_microservices()
        await register_microservice_routes(app, microservices)

        assert mongo_client.collection is not None, "MongoDB collection is not set during startup"

        await FastAPILimiter.init(redis_client)
        logger.info("Rate limiter initialized with Redis backend.")

        # Start RabbitMQ consumer in a separate thread to avoid blocking the application
        consumer_thread = Thread(target=start_rabbitmq_consumer, args=(container,))
        consumer_thread.daemon = True  # Daemon thread will exit when the main program exits
        consumer_thread.start()

        yield

    except Exception as e:
        logger.error(f"An error occurred during application startup: {e}")
        raise e

    finally:
        await mongo_client.disconnect()
        await redis_client.disconnect()
        logger.info("MongoDB and Redis clients disconnected during shutdown.")
