from django import template

register = template.Library()

@register.filter()
def censor(value):
    if not isinstance(value,str):
        raise ValueError('Тип должен быть строковый')

    ban_words = ['редиска', 'дурак', 'тварь']

    words = value.split()

    for i in range(len(words)):
        word = words[i]
        if word.lower() in ban_words:
            words[i] = '*' * len(word)

    censored_value = ' '.join(words)

    return censored_value



