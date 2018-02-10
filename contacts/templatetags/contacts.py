import string

from django import template

register = template.Library()

def is_ascii_printable(text):
    return all(ch in string.printable for ch in text)

@register.filter
def compact(value):
    """Compacts the location."""
    if not value:
        return value
    components = value.split('|')
    components = [c for c in components if c]
    if len(components) > 0 and components[0].endswith('洲'):
        del components[0]
    components = [x for x in components if x != '其他' and x != 'Other']
    if not components:
        return ''
    last = components[0]
    compacted = last
    for component in components[1:]:
        if is_ascii_printable(last) or is_ascii_printable(component):
            compacted += ' '
        compacted += component
    return compacted

@register.filter
def complete(value):
    """Complete the email address."""
    if not value:
        return value
    return value + '04@tsinghua.org.cn'

@register.filter
def gender(value):
    if value == 'M':
        return '男'
    elif value == 'F':
        return '女'
    else:
        return value
