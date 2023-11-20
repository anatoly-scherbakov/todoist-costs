from typing import Iterable

from rich.console import Console
from rich.table import Table

from todoist_costs.models import FinancialTask

MINIMUM_SAFE_BALANCE = 500


def format_balance(balance: float) -> str:
    formatted_balance = str(round(balance, 2))

    if balance < 0:
        formatted_balance = f'[red]{formatted_balance}[/red]'

    elif balance < MINIMUM_SAFE_BALANCE:
        formatted_balance = f'[orange1]{formatted_balance}[/orange1]'

    return formatted_balance


def print_report(tasks: Iterable[FinancialTask]):
    table = Table(
        'Date',
        'Task',
        'Raw amount',
        'Amount ($)',
        'Balance ($)',
    )

    for task in tasks:
        table.add_row(
            str(task.time.date()) if task.time else '',
            task.name,
            task.description,
            str(round(task.standardized_amount, 2)),
            format_balance(task.balance),
            style='green' if task.is_income else None,
        )

    Console().print(table)
