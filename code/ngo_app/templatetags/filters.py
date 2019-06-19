from django import template
register = template.Library()

@register.filter
def return_group(value):
    try:
        return value.groups.all()[0].name
    except IndexError:
        return "None"

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def bool_yay_nay(value: bool):
    if value is True:
        return "Yes"
    else:
        return "No"