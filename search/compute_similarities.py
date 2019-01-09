import html
from html.parser import HTMLParser
import spacy
import sklearn.preprocessing
from textacy.vsm import Vectorizer
from django.utils.text import slugify


def to_task_ids_and_descriptions(tasks):
    ids = []
    descriptions = []
    for _, task in tasks['taskMap'].items():
        ids.append(slugify(task['id']))
        english_description = task['title']['en'] + ' ' + task['description']['en']
        descriptions.append(english_description)
    return (ids, descriptions)


def to_service_ids_and_descriptions(services):
    ids = []
    descriptions = []
    for service in services:
        ids.append(service.id)
        description_without_markup = remove_double_escaped_html_markup(service.description)
        descriptions.append(service.name + ' ' + description_without_markup)
    return (ids, descriptions)


def remove_double_escaped_html_markup(data):
    unescaped_once = html.unescape(data)
    unescaped_twice = html.unescape(unescaped_once)

    remover = HTMLRemover()
    remover.feed(unescaped_twice)
    return remover.get_data()


class HTMLRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = False
        self.handled_data = []

    def handle_data(self, data):
        self.handled_data.append(data)

    def get_data(self):
        return ''.join(self.handled_data)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def error(self, message):
        raise RuntimeError(message)


def compute_similarities(docs):
    nlp = spacy.load('en')
    spacy_docs = [nlp(doc) for doc in docs]
    tokenized_docs = ([tok.lemma_ for tok in doc] for doc in spacy_docs)
    # lucene-style tf-idf
    vectorizer = Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth', apply_dl=True, dl_type='sqrt')
    term_matrix = vectorizer.fit_transform(tokenized_docs)
    return compute_cosine_doc_similarities(term_matrix)


def compute_cosine_doc_similarities(matrix):
    normalized_matrix = sklearn.preprocessing.normalize(matrix, axis=1)
    return normalized_matrix * normalized_matrix.T
