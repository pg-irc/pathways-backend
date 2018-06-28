def log_taxonomies(stream, tasks_fixture, articles_fixture):
    stream.write('\nTaxonomy terms for tasks\n\n')
    for key, value in tasks_fixture.items():
        taxonomy_terms = format_taxonomies(value)
        stream.write('{:<50} TaxTerms: {}'.format(key, taxonomy_terms))

    stream.write('\nTaxonomy terms for articles\n\n')
    for key, value in articles_fixture.items():
        taxonomy_terms = format_taxonomies(value)
        stream.write('{:<50} TaxTerms: {}'.format(key, taxonomy_terms))


def format_taxonomies(value):
    terms = value['taxonomyTerms']
    result = []
    for term in terms:
        result.append('{}:{}'.format(term['taxonomyId'], term['taxonomyTermId']))
    return ', '.join(result)


def log_locales(stream, tasks_fixture, articles_fixture):
    stream.write('\nLocales for tasks\n\n')
    for key, value in tasks_fixture.items():
        taxonomy_terms = format_locales(value)
        stream.write('{:<50} Locales: {}'.format(key, taxonomy_terms))

    stream.write('\nLocales for articles\n\n')
    for key, value in articles_fixture.items():
        taxonomy_terms = format_locales(value)
        stream.write('{:<50} Locales: {}'.format(key, taxonomy_terms))


def format_locales(value):
    title = get_sorted_keys(value['title'])
    description = get_sorted_keys(value['description'])
    if title == description:
        return ', '.join(title)
    return 'Inconsistent: title = {}, description = {}'.format(', '.join(title), ', '.join(description))


def get_sorted_keys(value):
    result = []
    for key in value:
        result.append(key)
    return sorted(result)
