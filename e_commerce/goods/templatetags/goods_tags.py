from django import template
from django.utils.http import urlencode



register = template.Library()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    """returns a dictionary of GET request parameters from the request object"""
    params = context['request'].GET.dict()
    params.update(kwargs)
    return urlencode(params)