from django import template
import re

register = template.Library()

@register.filter
def bold_words(content, words):
    if not words:
        return content
    words_list = words.split(',')
    for word in words_list:
        content = re.sub(r'({})'.format(re.escape(word.strip())), r'<strong>\1</strong>', content, flags=re.IGNORECASE)
    return content
