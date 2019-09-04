import csv

def build_manual_similarity_map(csv_data):
    result = {}

    if not csv_data:
        return result

    topics = csv_data[0]
    for topic_id in topics:
        result[topic_id] = []

    grid = csv_data[1:]
    for row in grid:
        column = 0
        for service_id in row:
            if service_id:
                topic_id = topics[column]
                result[topic_id].append(service_id)
            column += 1

    return result


def read_ids_one_per_line(file_path):
    with open(file_path) as file:
        content = file.readlines()
        return [x.strip() for x in content if x.strip() != '']
