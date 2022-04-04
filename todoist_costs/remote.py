from datetime import date
from time import strptime
from typing import Iterable, Tuple

import pendulum
import requests
from urlpath import URL

from todoist_costs.models import LabelSet, FinancialTask, TaskType


def retrieve(slug: str, token: str, **params):
    url = URL('https://api.todoist.com/rest/v1') / slug
    return url.get(
        headers={
            'Authorization': f'Bearer {token}',
        },
        timeout=7,
        params=params,
    ).json()


def retrieve_label_set(token: str) -> LabelSet:
    """Retrieve label IDs."""
    labels = retrieve(slug='labels', token=token)

    id_by_label = {
        item['name']: item['id']
        for item in labels
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
    tasks = retrieve(
        slug='tasks',
        token=token,
        filter='@cost, @income',
    )

    for task in tasks:
        task_type = TaskType.COST if (
            labels.cost in task['label_ids']
        ) else TaskType.INCOME

        due = task['due']
        raw_task_time = due.get('datetime') or due.get('date')
        task_time = pendulum.parse(raw_task_time)

        description = task['description']
        amount, currency = parse_description(description)

        amount = abs(amount)
        if task_type == TaskType.COST:
            amount = -amount

        yield FinancialTask(
            name=task['content'],
            description=description,
            amount=amount,
            currency=currency,
            time=task_time,
        )
