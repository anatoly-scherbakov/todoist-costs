from typing import Iterable

from rich.console import Console
from rich.table import Table

from todoist_costs.models import FinancialTask


def print_report(tasks: Iterable[FinancialTask]):
    table = Table(
        'Date',
        'Task',
        'Raw amount',
        'Amount (EUR)',
        'Balance (EUR)',
    )

    for task in tasks:
        table.add_row(
            str(task.time.date()) if task.time else '',
            task.name,
            task.description,
            str(round(task.standardized_amount, 2)),
            str(round(task.balance, 2)),
        )

    Console().print(table)
