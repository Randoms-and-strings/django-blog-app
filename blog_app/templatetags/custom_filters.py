from django import template

register = template.Library()


@register.filter(name='getitem')
def getitem(dictionary, key):
    """Access a dictionary's value by key."""
    if dictionary is None:
        return None
    return dictionary.get(key)