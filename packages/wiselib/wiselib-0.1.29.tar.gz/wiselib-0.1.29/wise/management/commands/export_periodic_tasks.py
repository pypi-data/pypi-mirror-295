import json
import logging
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from wise.station.registry import _ALL_PERIODIC_TASK_FIELDS, _UNSUPPORTED_PERIODIC_TASK_FIELDS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Export currently enabled PeriodicTasks"

    def handle(self, *args, **options):
        tasks = []

        for task in PeriodicTask.objects.filter(enabled=True):
            skip = False

            for field in _UNSUPPORTED_PERIODIC_TASK_FIELDS:
                if getattr(task, field) is not None:
                    skip = True
                    logger.warning(f"Unsupported field {field} found in task {task.name}, skipping this task")
                    break
            if skip:
                continue

            task_dict = {}
            for field in _ALL_PERIODIC_TASK_FIELDS:
                value = getattr(task, field, None)
                if value is None:
                    continue

                if field == "interval":
                    task_dict[field] = self._serialize_interval_schedule(value)
                else:
                    task_dict[field] = value

            tasks.append(task_dict)

        print(json.dumps(tasks, indent=4))

    @staticmethod
    def _serialize_interval_schedule(interval: IntervalSchedule) -> str:
        unit_mapping = {
            "days": "d",
            "hours": "h",
            "minutes": "m",
            "seconds": "s",
            "microseconds": "us",
        }
        return f"{interval.every}{unit_mapping[interval.period]}"
