from search.models import TaskSimilarityScores, TaskServiceSimilarityScores


def save_task_similarities(ids, similarities, count):
    TaskSimilarityScores.objects.all().delete()
    for i in range(len(ids)):
        sorted_scores = [similarities[i, j] for j in range(len(ids))]
        sorted_scores.sort(reverse=True)
        cutoff = sorted_scores[count]
        print('for task {}, similarity cutoff for related tasks is {}'.format(ids[i], cutoff))
        for j in range(len(ids)):
            score = similarities[i, j]
            if i != j and score >= cutoff:
                first_id = ids[i]
                second_id = ids[j]
                record = TaskSimilarityScores(first_task_id=first_id,
                                              second_task_id=second_id,
                                              similarity_score=score)
                record.save()


def save_task_service_similarity_scores(task_ids, service_ids, similarities, count):
    TaskServiceSimilarityScores.objects.all().delete()

    task_count = len(task_ids)
    service_count = len(service_ids)

    def to_service_offset(service_index):
        return task_count + service_index

    for task in range(task_count):
        sorted_scores_for_task = [similarities[task, to_service_offset(service)] for service in range(service_count)]
        sorted_scores_for_task.sort(reverse=True)
        cutoff = sorted_scores_for_task[count]
        print('for task {}, similarity cutoff for related services is {}'.format(task_ids[task], cutoff))
        for service in range(service_count):
            score = similarities[task, to_service_offset(service)]
            if score >= cutoff:
                task_id = task_ids[task]
                service_id = service_ids[service]
                record = TaskServiceSimilarityScores(task_id=task_id,
                                                     service_id=service_id,
                                                     similarity_score=score)
                record.save()
