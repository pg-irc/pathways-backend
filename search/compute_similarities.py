import re
import spacy
import sklearn.preprocessing
from textacy.vsm import Vectorizer
from django.utils.text import slugify
from spacy.lang.en.stop_words import STOP_WORDS as SPACY_STOP_WORDS


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
    tokenized_docs = ([token.lemma_.lower() for token in doc if not is_stop_word(token)] for doc in spacy_docs)
    # tf-idf
    vectorizer = Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth', apply_dl=False)
    term_matrix = vectorizer.fit_transform(tokenized_docs)
    save_intermediary_results_to_spreadsheet(vectorizer, term_matrix, topic_ids, service_ids)
    return compute_cosine_doc_similarities(term_matrix)


def is_stop_word(token):
    return (token.is_space or
            token.is_punct or
            token.is_bracket or
            token.like_num or
            # token.like_url or
            # token.like_email or
            token.lemma_ in STOPLIST)


def stop_list():
    stop_words = '''
    -PRON- and/or $
    Monday Tuesday Wednesday Thursday Friday Saturday Sunday Mon Tue Wed Thu Fri Sat Sun
    '''
    stop_words_set = set(stop_words.split())
    stop_words_set = stop_words_set.union(SPACY_STOP_WORDS)
    result = set([])
    for stop_word in stop_words_set:
        result.add(stop_word.lower())
    return result


STOPLIST = stop_list()


def save_intermediary_results_to_spreadsheet(vectorizer, term_matrix, topic_ids, service_ids):
    document_index = 0
    score_matrix = term_matrix.toarray()
    with open('output.csv', 'w') as file_handle:
        for document_id in topic_ids + service_ids:
            save_results_for_document(file_handle, vectorizer, score_matrix, document_index, document_id)
            document_index = document_index + 1


def save_results_for_document(file_handle, vectorizer, score_matrix, document_index, document_id):
    results = assemble_results_for_document(vectorizer, score_matrix, document_index)
    file_handle.write('"' + document_id + '"' + results + '\n')


def assemble_results_for_document(vectorizer, score_matrix, document_index):
    document_terms = get_document_terms(vectorizer, score_matrix, document_index)
    sorted_document_terms = sorted(document_terms, key=lambda term: term[1], reverse=True)
    return concatenate_terms_with_scores(sorted_document_terms)


def get_document_terms(vectorizer, score_matrix, document_index):
    document_terms = []
    for term_index in range(len(vectorizer.terms_list)):
        term = vectorizer.terms_list[term_index]
        score = score_matrix[document_index][term_index]
        if score > 0:
            document_terms.append((term, score))
    return document_terms


def concatenate_terms_with_scores(document_terms):
    result = ''
    for term in document_terms:
        result += ',"%s(%.2f)"' % (term[0].replace('\n', '\\n').replace('\t', '\\t'), term[1])
    return result


def compute_cosine_doc_similarities(matrix):
    normalized_matrix = sklearn.preprocessing.normalize(matrix, axis=1)
    return normalized_matrix * normalized_matrix.T


def remove_phone_numbers(description):
    if not description:
        return None
    return re.sub(r'(\+?[0-9]{1,2}-|\+?[\(\)\d]{3,5}-\d{3}-\d{4})', '', description)
