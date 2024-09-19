from django import template
import jdatetime

register = template.Library()


@register.filter(name="separate_thousands")
def separate_thousands(value):
    return "{:,}".format(int(value))
