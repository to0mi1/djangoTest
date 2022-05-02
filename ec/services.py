from ec.models import Item


def create_item(title: str, price: int):
    item = Item(title=title, price=price)
    item.save()
