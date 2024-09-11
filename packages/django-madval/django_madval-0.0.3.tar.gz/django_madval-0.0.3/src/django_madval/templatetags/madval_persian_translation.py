from django import template

register = template.Library()


WEEKDAYS = {
    'Sat': 'شنبه',
    'Sun': 'یکشنبه',
    'Mon': 'دوشنبه',
    'Tue': 'سه‌شنبه', # بین سه و شنبه از نیم فاصله استفاده شده
    'Wed': 'چهارشنبه',
    'Thu': 'پنجشنبه',
    'Fri': 'جمعه',
}
MONTHS = {
    'Far': 'فروردین',
    'Ord': 'اردیبهشت',
    'Kho': 'خرداد',
    'Tir': 'تیر',
    'Mor': 'مرداد',
    'Sha': 'شهریور',
    'Meh': 'مهر',
    'Aba': 'آبان',
    'Aza': 'آذر',
    'Dey': 'دی',
    'Bah': 'بهمن',
    'Esf': 'اسفند',
}


@register.filter(name='pn')
def persian_numbers_int(value):
    value = str(value)
    english_to_persian_table = value.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return value.translate(english_to_persian_table)


@register.filter(name='pnf')
def persian_numbers_float(value):
    value = str(value)
    english_to_persian_table = value.maketrans('0123456789.', '۰۱۲۳۴۵۶۷۸۹/')
    return value.translate(english_to_persian_table)


@register.filter(name='cspn')
def comma_separated_persian_numbers(value, separator=3):
    try:
        s = int(separator)
        separator = s if s>0 else 3
    except ValueError:
        separator = 3
    value = str(value)
    value = value.replace(' ', '')
    value = value.replace(',', '')
    value = value.replace('_', '')
    if len(value)==0:
        raise ValueError("The parameter you sent is empty!")
    for digit in value:
        if digit not in '0123456789۰۱۲۳۴۵۶۷۸۹.':
            raise ValueError("The parameter you sent is not a real number!"
            "Check special characters like '.', ',', '_', '/', '÷' and ..."
            " in sent number!")
    res = ''
    for i, char in enumerate(value[::-1]):
        res += char
        if i%separator==separator-1:
            res+=','
    if i%separator==separator-1:
        value = res[-2::-1]
    else:
        value = res[::-1]
    table = value.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return value.translate(table)


@register.filter(name='p_weekday')
def persian_weekday(value):
    day = str(value).capitalize()[:3]
    return WEEKDAYS.get(day, 'روز نامشخص از هفته')


@register.filter(name='p_month')
def persian_month(value):
    month = str(value).capitalize()[:3]
    return MONTHS.get(month, 'ماه نامشخص از سال')
