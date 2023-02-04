from typing import Iterable, Tuple

import pendulum
from requests import JSONDecodeError
from urlpath import URL

from todoist_costs.errors import MissingDueTime
from todoist_costs.models import LabelSet, FinancialTask, TaskType
from todoist_api_python.api import TodoistAPI

def retrieve(slug: str, token: str, **params):
    url = URL('https://api.todoist.com/rest/v1') / slug
    response = url.get(
        headers={
            'Authorization': f'Bearer {token}',
        },
        timeout=7,
        params=params,
    )

    response.raise_for_status()

    try:
        return response.json()
    except JSONDecodeError as err:
        raise ValueError(f'Invalid JSON: {response.text}\nError: {err}')


def retrieve_label_set(token: str) -> LabelSet:
    """Retrieve label IDs."""
    labels = TodoistAPI(token).get_labels()

    id_by_label = {
        label.name: label.id
        for label in labels
    }

    return LabelSet(
        cost=id_by_label['cost'],
        income=id_by_label['income'],
    )


def parse_description(description: str) -> Tuple[int, str]:
    """Parse task description into amount and currency."""
    raw_amount, currency = description.split(' ')

    raw_amount = raw_amount.replace('k', '000')

    return int(raw_amount), currency


def retrieve_tasks(token: str, labels: LabelSet) -> Iterable[FinancialTask]:
    tasks = TodoistAPI(token).get_tasks(
        filter='@cost, @income',
    )

    for task in tasks:
        task_type = TaskType.COST if 'cost' in task.labels else TaskType.INCOME

        due = task.due

        if due is None:
            raise MissingDueTime(
                task_name=task.content,
                task_url=task.url,
            )

        raw_task_time = due.datetime or due.date
        task_time = pendulum.parse(raw_task_time)

        description = task.description
        amount, currency = parse_description(description)

        amount = abs(amount)
        if task_type == TaskType.COST:
            amount = -amount

        yield FinancialTask(
            name=task.content,
            description=description,
            amount=amount,
            currency=currency,
            time=task_time,
        )
