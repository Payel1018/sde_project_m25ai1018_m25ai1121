from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    exchanger: str = "amq.direct"
    queue_name_to_first_service: str = "notify_user"
    queue_name_to_second_service: str = "changebalance_orders"

    routing_key_to_first_service: str = "user.mailing"
    routing_key_to_second_service: str = "orders.checkout"
