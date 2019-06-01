import logging
from search.models import Task, TaskSimilarityScore, TaskServiceSimilarityScore
from human_services.services.models import Service

LOGGER = logging.getLogger(__name__)


def save_task_similarities(ids, similarities, count):
    TaskSimilarityScore.objects.all().delete()
    for i in range(len(ids)):
        similarities_for_task = [similarities[i, j] for j in range(len(ids)) if i != j]
        cutoff = compute_cutoff(similarities_for_task, count)
        for j in range(len(ids)):
            score = similarities[i, j]
            if i != j and score >= cutoff:
                record = TaskSimilarityScore(first_task_id=ids[i],
                                             second_task_id=ids[j],
                                             similarity_score=score)
                record.save()


def compute_cutoff(scores, count):
    scores.sort(reverse=True)
    return scores[min(count, len(scores)) - 1]


def save_task_service_similarity_scores(task_ids, service_ids, similarities, count):
    TaskServiceSimilarityScore.objects.all().delete()
    task_count = len(task_ids)
    service_count = len(service_ids)

    # Assuming that the similarities are computed from a document vector
    # containing topic descriptions *followed by* service descriptions
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


def save_manual_similarities(manual_similarities):
    manual_similarity_score = 1.0
    for topic_id, service_ids in manual_similarities.items():
        for service_id in service_ids:
            if is_task_id_valid(topic_id) and is_service_id_valid(service_id):
                TaskServiceSimilarityScore.objects.update_or_create(
                    task_id=topic_id,
                    service_id=service_id,
                    defaults={
                        'similarity_score': manual_similarity_score
                    }
                )


def is_task_id_valid(topic_id):
    try:
        Task.objects.get(id=topic_id)
        return True
    except Task.DoesNotExist:
        LOGGER.warning('%s: Failed to save manual similarity, no such topic', topic_id)
        return False


def is_service_id_valid(service_id):
    try:
        Service.objects.get(id=service_id)
        return True
    except Service.DoesNotExist:
        LOGGER.warning('%s: Failed to save manual similarity, no such service', service_id)
        return False
