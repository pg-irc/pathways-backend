from search.models import TaskSimilarityScore, TaskServiceSimilarityScore


def save_task_similarities(ids, similarities, count):
    TaskSimilarityScore.objects.all().delete()
    for i in range(len(ids)):
        similarities_for_task = [similarities[i, j] for j in range(len(ids))]
        cutoff = compute_cutoff(similarities_for_task, count)
        for j in range(len(ids)):
            score = similarities[i, j]
            if i != j and score >= cutoff:
                record = TaskSimilarityScore(first_task_id=ids[i],
                                             second_task_id=ids[j],
                                             similarity_score=score)
                record.save()


def compute_cutoff(scores, element_count):
    scores.sort(reverse=True)
    return scores[element_count]


def save_task_service_similarity_scores(task_ids, service_ids, similarities, count):
    TaskServiceSimilarityScore.objects.all().delete()
    task_count = len(task_ids)
    service_count = len(service_ids)

    # Assuming that the similarities are computed from a document vector
    # containing task descriptions *followed by* service descriptions
    def to_service_similarity_offset(service_index):
        return task_count + service_index

    for i in range(task_count):
        similarities_for_task = [similarities[i, to_service_similarity_offset(j)]
                                 for j in range(service_count)]
        cutoff = compute_cutoff(similarities_for_task, count)
        for j in range(service_count):
            score = similarities[i, to_service_similarity_offset(j)]
            if score >= cutoff:
                record = TaskServiceSimilarityScore(task_id=task_ids[i],
                                                    service_id=service_ids[j],
                                                    similarity_score=score)
                record.save()
