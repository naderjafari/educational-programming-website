from django import template
import jdatetime

register = template.Library()


@register.filter(name="to_jalali")
def to_jalali(value):
    if value:
        return jdatetime.datetime.fromgregorian(datetime=value).strftime("%d %B %Y")
    return ""
