from search.models import TaskSimilarityScores, TaskServiceSimilarityScores


def save_task_similarities(ids, similarities):
    TaskSimilarityScores.objects.all().delete()
    for i in range(len(ids)):
        for j in range(len(ids)):
            if i != j:
                first_id = ids[i]
                second_id = ids[j]
                score = similarities[i, j]
                record = TaskSimilarityScores(first_task_id=first_id,
                                              second_task_id=second_id,
                                              similarity_score=score)
                record.save()


def save_task_service_similarity_scores(task_ids, service_ids, similarities):
    TaskServiceSimilarityScores.objects.all().delete()
    for task_index in range(len(task_ids)):
        for service_index in range(len(service_ids)):
            task_offset = task_index
            service_offset = len(task_ids) + service_index

            task_id = task_ids[task_index]
            service_id = service_ids[service_index]
            score = similarities[task_offset, service_offset]

            record = TaskServiceSimilarityScores(task_id=task_id,
                                                 service_id=service_id,
                                                 similarity_score=score)
            record.save()
