from django import template

register = template.Library()

@register.filter
def splitcon(value):
    return value.split(",")