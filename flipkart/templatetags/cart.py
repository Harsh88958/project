from django import template

register = template.Library()


@register.filter(name="is_exist_in_cart")
def is_exist_in_cart(product, cart):
    keys = cart.keys()
    for key in keys:
        if int(key) == product.id:
            return True
        return False


@register.filter(name="cart_quantity")
def cart_quantity(product, cart):
    keys = cart.keys()
    for key in keys:
        if int(key) == product.id:
            return cart.get(key)


@register.filter(name="total_price")
def total_price(product, cart):
    tp = product.product_price * cart_quantity(product, cart)
    return tp


@register.filter(name="payable_amount")
def payable_amount(product, cart):
    s = 0
    for pro in product:
        s = s + total_price(pro, cart)
    return s


@register.filter(name="ord_details")
def ord_details(price, quantity):
    return price * quantity
