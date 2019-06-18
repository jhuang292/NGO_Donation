from django import template
register = template.Library()

@register.filter
def return_group(value):
    try:
        return value.groups.all()[0].name
    except IndexError:
        return "None"
