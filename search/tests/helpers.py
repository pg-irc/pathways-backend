from common.testhelpers.random_test_values import a_float


def create_square_matrix_of_unique_floats(number):
    while True:
        scores = [[a_float() for i in range(number)] for j in range(number)]
        if not is_a_duplicate_score_in_square_matrix(scores):
            return scores


def is_a_duplicate_score_in_square_matrix(scores):
    float_dictionary = {}

    for i in scores:
        for j in i:
            if j in float_dictionary:
                return True      
            float_dictionary[j] = 1    
    return False