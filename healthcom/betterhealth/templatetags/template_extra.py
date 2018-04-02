from django import template

register = template.Library()

@register.filter(name='ellipses')
def ellipses(value, arg):
    original_string = value
    max_length = arg

    if len(original_string) <= max_length:
        return original_string
    else:
        return original_string[:max_length] + "..."

