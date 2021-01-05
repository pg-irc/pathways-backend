import re

# BC211's convention for marking records as inactive is DEL + number or DEL + whitespace + number

def is_inactive(description):
    return description and description_starts_with_inactive_record_convention(description)


def description_starts_with_inactive_record_convention(description):
    stripped_description = description.strip()
    return re.search(r'^DEL[0-9\s]', stripped_description, flags=re.IGNORECASE)
