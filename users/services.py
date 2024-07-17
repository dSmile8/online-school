
import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(amount, product):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product.get("name")},
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
