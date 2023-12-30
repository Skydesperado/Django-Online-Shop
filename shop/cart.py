from shop.models import Product

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        if not isinstance(CART_SESSION_ID, str):
            raise ValueError("CART_SESSION_ID Must Be a String")
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_ID, {})

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["total_price"] = float(item["price"]) * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price)
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def get_total_price(self):
        return sum(
            float(item["price"]) * item["quantity"]
            for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = max(
                0, self.cart[product_id]["quantity"] - 1)
            if self.cart[product_id]["quantity"] == 0:
                del self.cart[product_id]
            self.save()

    def clear(self):
        self.session.pop(CART_SESSION_ID, None)
        self.save()
