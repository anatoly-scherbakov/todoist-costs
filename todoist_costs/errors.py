from dataclasses import dataclass

from documented import DocumentedError


@dataclass(frozen=True)
class MissingDueTime(DocumentedError):
    """
    Due date or time missing for a cost-related Todoist task.

      * Task name: {self.task_name}
      * Task URL: {self.task_url}

    Please add a due date.
    """

    task_name: str
    task_url: str
