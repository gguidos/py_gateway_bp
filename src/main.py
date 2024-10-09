from fastapi import FastAPI
import uvicorn
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.exception_handlers import register_exception_handlers
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.response_interceptor import ResponseFormatMiddleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.infrastructure.logging_config import setup_logging
from src.infrastructure.di_container import Container
from src.utils.dynamic_router import register_microservice_routes 
from src.interfaces.api.v1.gateway_controller import router as gateway_controller
from src.interfaces.api.v1.microservice_controller import router as microservice_controller
from src.middleware.request_id_middleware import RequestIDMiddleware
from src.services.ms_service import MicroserviceService
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging configuration
setup_logging()

# Initialize the logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Gateway Microservice",
    description="A gateway service for routing and managing API requests",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
# Register the middleware to intercept all responses
app.add_middleware(ResponseFormatMiddleware)

# Add the Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Initialize the DI container
container = Container()
container.config.db_uri.from_env("MONGO_URI")
container.config.db_name.from_env("DB_NAME")
container.config.db_collection.from_env("DB_COLLECTION")
container.config.redis_host.from_env("REDIS_HOST", default="localhost")
container.config.redis_port.from_env("REDIS_PORT", default=6379)
container.config.redis_db.from_env("REDIS_DB", default=0)
container.config.redis_password.from_env("REDIS_PASSWORD", default=None)

container.init_resources()

# Wire the container to the modules that use the dependencies
container.wire(modules=["src.interfaces.api.v1.gateway_controller"])  # Wire the gateway controller
container.wire(modules=["src.interfaces.api.v1.microservice_controller"])  # Wire the user controller

app.container = container

app.include_router(gateway_controller, prefix="/api/v1", tags=["gateway"])
app.include_router(microservice_controller, prefix="/api/v1", tags=["microservice"])

# Register global exception handlers
register_exception_handlers(app)

# Use an async context manager for lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event manager to handle startup and shutdown events."""
    try:
        # Startup event to connect to Redis and MongoDB when the application starts
        mongo_client = container.mongo_client()
        await mongo_client.connect()
        redis_client = container.redis_client()
        await redis_client.connect()
        logger.info("MongoDB and Redis clients connected during startup.")
        
        # Assume we have a service to get all microservices from the database
        microservice_service: MicroserviceService = container.microservice_service()
        microservices = await microservice_service.get_all_microservices()  # Retrieve all microservices

        # Register microservice routes dynamically
        await register_microservice_routes(app, microservices)

        # Verify that the MongoDB collection is set correctly
        assert mongo_client.collection is not None, "MongoDB collection is not set during startup"

        # Initialize FastAPILimiter if you have rate limiting
        await FastAPILimiter.init(redis_client)
        logger.info("Rate limiter initialized with Redis backend.")

        # Yield control to allow handling requests
        yield

    except Exception as e:
        logger.error(f"An error occurred during application startup: {e}")
        raise e

    finally:
        # Shutdown event to disconnect from Redis and MongoDB when the application shuts down
        await mongo_client.disconnect()
        await redis_client.disconnect()
        logger.info("MongoDB and Redis clients disconnected during shutdown.")

# Set lifespan event handler for the FastAPI application
app.router.lifespan_context = lifespan

def server_started(server):
    for server in server.servers:
        for socket in server.sockets:
            print(socket.getsockname())


def main():
    config = uvicorn.Config("main:app", port=8500)
    server = uvicorn.Server(config)

    orig_log_started_message = server._log_started_message

    def patch_log_started_message(listeners):
        orig_log_started_message(listeners)
        server_started(server)

    server._log_started_message = patch_log_started_message

    server.run()


if __name__ == "__main__":
    main()