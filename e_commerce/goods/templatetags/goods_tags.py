from django import template
from django.utils.http import urlencode



register = template.Library()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    """returns a dictionary of GET request parameters from the request object"""
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)