import re

def is_inactive(description):
    # This is BC211's convention for marking records as inactive
    return description and description_starts_with_inactive_record_convention(description)

def description_starts_with_inactive_record_convention(description):
    stripped_description = description.strip()
    return re.search(r'^[D-d-E-e-L-l]{3}[0-9]', stripped_description)