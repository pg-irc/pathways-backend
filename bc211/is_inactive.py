def is_inactive(record):
    # This is BC211's convention for marking records as inactive
    return record.description and record.description.strip().startswith('DEL')
