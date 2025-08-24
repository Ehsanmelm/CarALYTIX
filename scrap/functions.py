# utils/converters.py

def persian_to_english_number(value):

    if value is None:
        return value

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"

    translation_table = {}

    # Map Persian
    for p, e in zip(persian_digits, english_digits):
        translation_table[ord(p)] = e

    # Map Arabic
    for a, e in zip(arabic_digits, english_digits):
        translation_table[ord(a)] = e

    # Replace digits
    value = str(value).translate(translation_table)

    # Convert to float if it looks like a number
    try:
        return float(value)
    except ValueError:
        return value
