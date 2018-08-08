from django import template

register = template.Library()

@register.filter
def abc(value):
    return value.split("|")