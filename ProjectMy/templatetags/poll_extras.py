from django import template
register = template.Library()

@register.simple_tag
def max_number(*args):
    return max(args)

@register.filter
def power(number1, number2):
    return number1**number2
