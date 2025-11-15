from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    exchanger: str = "amq.direct"
    queue_name_to_cart_order: str = "user_cart"
    queue_name_to_second_service: str = "changebalance_orders"

    routing_key_to_cart_order: str = "user.cart"
    routing_key_to_second_service: str = "orders.checkout"
