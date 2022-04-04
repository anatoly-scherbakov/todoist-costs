import operator
from dataclasses import replace
from typing import Iterable

from todoist_costs.models import FinancialTask


def calculate(tasks: Iterable[FinancialTask]) -> Iterable[FinancialTask]:
    balance = 0

    for task in tasks:
        balance += task.standardized_amount

        yield replace(
            task,
            balance=balance,
        )
