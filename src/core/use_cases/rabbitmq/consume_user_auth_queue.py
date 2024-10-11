from src.core.repositories.rabbitmq_repository import RabbitMQRepository

class ConsumeUserAuthQueue:
    def __init__(self, repository: RabbitMQRepository):
        self.repository = repository

    def execute(self, on_message_callback):
        queue_name = 'user_auth_queue'
        return self.repository.consume_queue(queue_name, on_message_callback)
