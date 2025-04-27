from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def query_string(context):
    params = context['request'].GET.copy()
    params.pop('page', None)
    return params.urlencode()
