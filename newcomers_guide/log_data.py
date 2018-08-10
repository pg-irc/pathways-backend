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
    if 'taxonomyTerms' not in value:
        return '---------------- NO TAXONOMY TERMS IN THIS ITEM ----------------'
    terms = value['taxonomyTerms']
    result = []
    for term in terms:
        result.append('{}:{}'.format(term['taxonomyId'], term['taxonomyTermId']))
    return ', '.join(result)


def log_locales(stream, tasks_fixture, articles_fixture):
    stream.write('\nLocales for tasks\n\n')
    lines = build_and_sort_locale_log_lines(tasks_fixture)
    print_log_lines(stream, lines)

    stream.write('\nLocales for articles\n\n')
    lines = build_and_sort_locale_log_lines(articles_fixture)
    print_log_lines(stream, lines)


class LogLine:
    def __init__(self, chapter, theId, logdata):
        self.chapter = chapter
        self.id = theId
        self.logdata = logdata


def key_for_sorting(log_line):
    return '{}:{}'.format(log_line.chapter, log_line.id)


def build_and_sort_locale_log_lines(tasks_fixture):
    log_lines = []
    for key, value in tasks_fixture.items():
        locales = format_locales(value)
        logdata = '{:<50} Locales: {}'.format(key, locales)
        log_lines.append(LogLine(value['chapter'], value['id'], logdata))

    return sorted(log_lines, key=key_for_sorting)


def print_log_lines(stream, log_lines):
    chapter = ''
    for line in log_lines:
        if chapter != line.chapter:
            stream.write('\nChapter {}:\n\n'.format(line.chapter))
            chapter = line.chapter

        stream.write(line.logdata)


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
