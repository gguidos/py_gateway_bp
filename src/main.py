from fastapi import FastAPI
import uvicorn
from src.infrastructure.di_container import Container
from src.utils.system.config import load_config
from src.utils.system.lifespan import lifespan
from src.utils.system.middleware_setup import add_middlewares
from src.utils.system.routes import register_routers
from src.infrastructure.exception_handlers import register_exception_handlers
from src.infrastructure.logging_config import setup_logging
import logging

# Setup logging configuration
setup_logging()

# Initialize the logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Gateway Microservice",
    description="A gateway service for routing and managing API requests",
    version="1.0.0"
)

# Initialize the DI container
container = Container()
load_config(container)
container.init_resources()

# Attach DI container to the app
app.container = container

# Register middlewares
add_middlewares(app)

# Register routers
register_routers(app)

# Register global exception handlers
register_exception_handlers(app)

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
