from market.models import ProductProxy


class Cart:
    def __init__(self, request)-> None:
        self.session = request.session

        cart = self.session.get('session_key')

        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] ={'qty': quantity, 'price': str(product.price)}


            def add(self, product, quantity):
                product_id = str(product.id)

                if product_id not in self.cart:
                    self.cart[product_id] = {'qty':quantity, 'price': str(product.price)}