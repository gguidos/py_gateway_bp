# API Gateway Microservice

Welcome to the **API Gateway Microservice** repository! This project is a foundational template for building a gateway service that routes, filters, and handles requests between various microservices in a distributed architecture.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
  - [Local Development](#local-development)
  - [Using Docker](#using-docker)
- [Endpoints](#endpoints)
- [Rate Limiting and Throttling](#rate-limiting-and-throttling)
- [Metrics and Monitoring](#metrics-and-monitoring)
- [Security](#security)
  - [Security Headers](#security-headers)
  - [Input Sanitization](#input-sanitization)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **FastAPI** framework for high-performance API gateway routing.
- **Dynamic Route Registration**  Automatically register routes for microservices based on their configuration stored in MongoDB.
- **Dynamic Proxy Routing** Proxy requests to different microservices using dynamic routing based on configurations stored in the database.
- **Microservice Registration** Supports registering new microservices dynamically through a dedicated API.
- **Rate Limiting** with Redis using `fastapi-limiter`.
- **Dependency Injection** using `dependency-injector` for modular and maintainable code.
- **Request/Response Validation** with Pydantic models.
- **Centralized Exception Handling** Consistent and unified error handling across the gateway with custom exceptions and global exception handlers.
- **MongoDB Integration** Stores microservice configurations, paths, and other metadata.
- **Redis Integration** Used for rate limiting and caching.
- **Custom Middleware** for logging, request tracking, and security.
- **Unified Logging** configuration with support for JSON and file-based logging.
- **Structured Project Layout** following Clean Architecture principles.
- **API Key Management** for securing the endpoints.
- **Metrics and Monitoring** with Prometheus integration.
- **Health Checks** and **Readiness Probes** for service monitoring.

## Project Structure

```bash
gateway-service/
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── logs
├── project_structure.txt
├── requirements.txt
├── src
│   ├── core
│   │   ├── entities
│   │   │   ├── base_entity.py
│   │   │   └── microservice.py
│   │   ├── repositories
│   │   │   └── db_repository.py
│   │   ├── schemas
│   │   │   └── microservice_schema.py
│   │   ├── services
│   │   └── use_cases
│   │       ├── create_ms.py
│   │       ├── get_all_ms.py
│   │       └── get_ms.py
│   ├── dependencies
│   │   ├── microservice_service_dependency.py
│   │   └── request_id_dependency.py
│   ├── infrastructure
│   │   ├── db
│   │   │   ├── mongo_client.py
│   │   │   └── redis_client.py
│   │   ├── di_container.py
│   │   ├── exception_handlers.py
│   │   └── logging_config.py
│   ├── interfaces
│   │   └── api
│   │       └── v1
│   │           ├── gateway_controller.py
│   │           ├── health_check.py
│   │           └── microservice_controller.py
│   ├── main.py
│   ├── middleware
│   │   ├── logging_middleware.py
│   │   ├── request_id_middleware.py
│   │   ├── response_interceptor.py
│   │   └── security_headers.py
│   ├── services
│   │   ├── gateway_service.py
│   │   ├── get_ms_services.py
│   │   └── ms_service.py
│   └── utils
│       └── dynamic_router.py
└── tests
    └── post.http

19 directories, 32 files
```


- src/: The core directory containing service logic and configuration.
- dependencies/: Contains dependency injection-related files.
- infrastructure/: Handles database clients, DI containers, and external integrations.
- interfaces/: Contains API routers, controllers, and request/response models.
- middlewares/: Custom middleware files for request tracking, logging, and security.
- services/: Core business logic and service orchestration.
- tests/: Unit and integration test files for various components.

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.8 or higher
- MongoDB 4.0 or higher
- Redis 5.0 or higher
- Docker (optional, for running via Docker)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install MongoDB locally** or ensure a remote instance is accessible.

### Environment Setup

1. **Create a `.env` file** in the root of the project and set up the following environment variables:

    ```ini
    MONGO_URI=mongodb://localhost:27017
    DB_NAME=gateway_db
    DB_COLLECTION=routes
    REDIS_URL=redis://localhost:6379/0
    LOG_LEVEL=DEBUG
    ```

2. **Modify the `.env` file** according to your local or production configurations.

## Running the Application

### Local Development

1. **Start MongoDB and Redis server** if running locally:

    ```bash
    mongod
    redis-server
    ```

2. **Run the application:**

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8500 --reload
    ```

3. The API will be available at `http://127.0.0.1:8500`.

### Using Docker

1. **Build the Docker image:**

    ```bash
    docker build -t gateway-service .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 --env-file .env gateway-service
    ```

## Endpoints

Here are some key endpoints provided by this boilerplate:

- `GET /api/v1/microservice`: Retrieve all available routes.
- `POST /api/v1/microservice`: Register a new microservice dynamically.
- `GET /internal/metrics`: Prometheus metrics endpoint.
- `GET /api/v1/health`: Health endpoint.
- `GET /api/v1/readiness`: Readiness endpoint.


## Sample Request to Register a Microservice

- `POST /api/v1/microservice/`

```json
{
  "service_name": "user-service",
  "base_url": "http://localhost:8000",
  "paths": [
    {
      "path": "/users",
      "method": "GET",
      "protected": true,
      "rate_limit": {
        "requests_per_minute": 10,
        "requests_per_hour": 100
      }
    }
  ],
  "api_key": "some-api-key"
}
```

### Response Format

```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed successfully."
}
```

```json
{
  {
  "status": "success",
  "data": {
    "id": "5f87bffcb0c050e5e90cbf94",
    "service_name": "user-service",
    "base_url": "http://localhost:8000",
    "paths": [
      {
        "path": "/users",
        "method": "GET",
        "protected": true,
        "rate_limit": {
          "requests_per_minute": 10,
          "requests_per_hour": 100
        }
      }
    ],
    "api_key": "some-api-key"
  },
  "message": "Microservice registered successfully."
}
}
```

## Security and Rate Limiting

- `API Key Management`: An X-API-Key header is used for validating access to secure endpoints. The key is defined in the .env file.

- `Rate Limiting`: Middleware to limit the number of requests a client can make in a defined time window. See rate_limiting_middleware.py.

- `Security Headers`: Content-Security-Policy, Strict-Transport-Security, and X-Content-Type-Options headers are added using the security_config.py.

## Metrics, Monitoring, and Health Checks

- `Prometheus Metrics`: /internal/metrics endpoint provides real-time metrics. See metrics.py.

- `Health Checks`: /api/v1/health endpoint provides application health status.

- `Readiness Checks`: /api/v1/readiness endpoint provides database health status.

- `Monitoring & Alerting`: Use Prometheus and Alertmanager for monitoring and alerting setups.

## Testing
To run the tests, make sure you have pytest installed:

```bash
pytest
```
