from django import template
import random

register = template.Library()

@register.filter(name='shuffle')
def shuffle(value):
    shuffled = list(value)
    random.shuffle(shuffled)
    return shuffled


@register.filter
def slice_list(value, arg):
    """
    Slices a list.
    Usage: {{ some_list|slice_list:"start:end" }}
    Example: {{ mylist|slice_list:"0:3" }}
    """
    try:
        start, end = map(int, arg.split(':'))
        return value[start:end]
    except (ValueError, TypeError):
        return value

@register.filter
def discount_amount(product):
    """
    Calculate the discount amount.
    """
    if product.discount and product.price:
        return int(product.price * (product.discount / 100))
    return 0

@register.filter
def price_before_discount(product):
    """
    Calculate the price before the discount was applied.
    """
    if product.discount and product.price:
        discount_amount = product.price * (product.discount / 100)
        return product.price + discount_amount
    return product.price

@register.filter
def discount_percentage(discount):
    """
    Format the discount percentage to an integer.
    """
    return int(discount)
