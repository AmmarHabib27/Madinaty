import re


def normalize_phone(value: str) -> str:
    cleaned = re.sub(r'[^\d+]', '', value)
    if cleaned.startswith('+'):
        return cleaned
    if cleaned.startswith('00') and len(cleaned) > 2:
        return '+' + cleaned[2:]
    if cleaned.startswith('0') and len(cleaned) >= 11:
        return '+20' + cleaned[1:]
    return value
