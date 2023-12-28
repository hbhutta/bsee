import re

def remove_utf(text: str):
    prepared_text = text
    for i in range(0, len(text)):
        if text[i] == '\\':
            prepared_text = text[:i+1] + '\\' + text[i+2:]
    pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
    cleaned_text = pattern.sub('', prepared_text)
    return cleaned_text

def find_phone_numbers(text: str) -> list[str]:
    pattern = re.compile(r'\b\d{3}-\d{3}-\d{4}')
    phone_numbers = pattern.findall(pattern, text)
    return phone_numbers