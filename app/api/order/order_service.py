from app.models import Order, Product, Storehouse


class OrderService:
    """ Бизнес логика заказов"""
    def __init__(self, order: Order, product: Product, storehouse: Storehouse, logisitcs):
        self.order = order
        self.product = product
        self.storehouse = storehouse
        self.logistics = logisitcs

    def create_order(self, user_id: int, city_id: int, items: list, delivery_adress: str):
        pass

    def return_order(self, order_id: int, user_id: int, city_id: int):
        pass

    def get_order_status(self, order_id: int):
        pass
