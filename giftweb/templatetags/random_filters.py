from django import template
import random

register = template.Library()

@register.filter(name='shuffle')
def shuffle(value):
    shuffled = list(value)
    random.shuffle(shuffled)
    return shuffled
