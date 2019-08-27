# Read CSV

def read_manual_similarities(csv_path):
    result = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            result.append(row)
    return result


# Handle lines from CSV
# Remove similarity score for topic/service pair
# Set similarity score for topic/service pair
