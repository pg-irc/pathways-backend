import csv


def read_manual_similarities(csv_path):
    result = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            result.append(row)
    return result


def build_manual_similarity_map(csv_data):
    result = {}

    topics = csv_data[0]
    for topic in topics:
        result[topic] = []

    grid = csv_data[1:]
    for row in grid:
        column = 0
        for cell in row:
            topic = topics[column]
            if cell:
                result[topic].append(cell)
            column += 1

    return result
