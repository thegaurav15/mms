from django import template
import decimal

register = template.Library()

@register.filter()
def verbose_name(object_name, field_name):
    return object_name._meta.get_field(field_name).verbose_name

@register.filter()
def rs_in_words(amount):
    return num2words(amount)

def num2words(num):
    num = decimal.Decimal(num)
    decimal_part = (num - int(num)) * 100
    num = int(num)

    if decimal_part:
        return num2words(num) + " and " + num2words(decimal_part) + " " + ("paise" if decimal_part>1 else "paisa")

    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

    if num < 20:
        return under_20[num]

    if num < 100:
        return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot==0 else ' ' + num2words(num % pivot))
