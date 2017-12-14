from collections import defaultdict
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

class ImportProgress(object):
    PROGRESS_ERROR = 0
    PROGRESS_NEW = 1
    PROGRESS_SKIP = 2

    def __init__(self):
        self._totals = defaultdict(int)
        self._counts = defaultdict(lambda: defaultdict(int))

    def add_total(self, group):
        self._totals[group] += 1

    def add_error(self, group):
        self.add_total(group)
        self._counts[group][self.PROGRESS_ERROR] += 1

    def add_new(self, group):
        self.add_total(group)
        self._counts[group][self.PROGRESS_NEW] += 1

    def add_skip(self, group):
        self.add_total(group)
        self._counts[group][self.PROGRESS_SKIP] += 1

    def __str__(self):
        return " | ".join(
            self._format_model_counts()
        )

    def _format_model_counts(self):
        for (model, counts) in self._counts.items():
            numbers_list = []

            total_count = self._totals[model]
            numbers_list.append(
                str(total_count)
            )

            new_count = counts[self.PROGRESS_NEW]
            if new_count:
                numbers_list.append(
                    ungettext("({} new)", "({} new)", new_count).format(
                        new_count
                    )
                )

            error_count = counts[self.PROGRESS_ERROR]
            if error_count:
                numbers_list.append(
                    ungettext("({} error)", "({} errors)", error_count).format(
                        error_count
                    )
                )

            yield _("{model}: {numbers}").format(
                model=model,
                numbers=" ".join(numbers_list)
            )
