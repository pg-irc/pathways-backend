import re
import spacy
import sklearn.preprocessing
from textacy.vsm import Vectorizer
from django.utils.text import slugify


def to_topic_ids_and_descriptions(topics):
    ids = []
    descriptions = []
    i = 0
    for _, topic in topics['taskMap'].items():
        ids.append(slugify(topic['id']))
        english_description = topic['title']['en'] + ' ' + topic['description']['en']
        descriptions.append(english_description)
        i = i + 1
        if i == 10:
            return (ids, descriptions)
    return (ids, descriptions)


def to_service_ids_and_descriptions(services):
    ids = []
    descriptions = []
    for service in services:
        ids.append(service.id)
        description_without_phone_numbers = remove_phone_numbers(service.description) or ''
        descriptions.append(service.name + ' ' + description_without_phone_numbers)
    return (ids, descriptions)


def compute_similarities(docs, topic_ids, service_ids):
    nlp = spacy.load('en')
    spacy_docs = [nlp(doc) for doc in docs]
    tokenized_docs = ([tok.lemma_ for tok in doc] for doc in spacy_docs)
    # tf-idf
    vectorizer = Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth', apply_dl=False)
    term_matrix = vectorizer.fit_transform(tokenized_docs)
    save_intermediary_results_to_spreadsheet(vectorizer, term_matrix, topic_ids, service_ids)
    return compute_cosine_doc_similarities(term_matrix)


def save_intermediary_results_to_spreadsheet(vectorizer, term_matrix, topic_ids, service_ids):
    score_matrix = term_matrix.toarray()
    document_index = 0
    for document_id in topic_ids + service_ids:
        document_terms = get_document_terms(vectorizer, score_matrix, document_index)
        document_terms = sorted(document_terms, key=lambda term: term[1], reverse=True)
        line = make_line(document_terms)
        print('"' + document_id + '"' + line)
        document_index = document_index + 1


def get_document_terms(vectorizer, score_matrix, document_index):
    document_terms = []
    for term_index in range(len(vectorizer.terms_list)):
        term = vectorizer.terms_list[term_index]
        score = score_matrix[document_index][term_index]
        if score > 0:
            document_terms.append((term, score))
    return document_terms


def make_line(document_terms):
    line = ''
    for term in document_terms:
        line += ',"%s (%s)"' % (term[0].replace('\n', '\\n'), term[1])
    return line


def compute_cosine_doc_similarities(matrix):
    normalized_matrix = sklearn.preprocessing.normalize(matrix, axis=1)
    return normalized_matrix * normalized_matrix.T


def remove_phone_numbers(description):
    if not description:
        return None
    return re.sub(r'(\+?[0-9]{1,2}-|\+?[\(\)\d]{3,5}-\d{3}-\d{4})', '', description)
