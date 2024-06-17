from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)  # Return None if key is not found
