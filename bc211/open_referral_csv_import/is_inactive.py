def is_inactive(description):
    # This is BC211's convention for marking records as inactive
    return description and description.strip().startswith('DEL')
