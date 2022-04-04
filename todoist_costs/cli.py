import datetime
import itertools
import operator
from typing import List

from typer import Typer, Option, Argument

from todoist_costs.finance import calculate
from todoist_costs.models import FinancialTask
from todoist_costs.remote import retrieve_label_set, retrieve_tasks, \
    parse_description
from todoist_costs.ui import print_report

app = Typer()


@app.command()
def report(
    token: str = Option(default=..., envvar='TODOIST_TOKEN'),
    balance: List[str] = Argument(...),
):
    """Financial report based on planned income and costs."""
    parsed_balance = list(map(parse_description, balance))
    balance_tasks = [FinancialTask(
        name='',
        amount=amount,
        currency=currency,
        time=None,
        description=f'{amount} {currency}',
    ) for amount, currency in parsed_balance]

    label_set = retrieve_label_set(token)
    tasks = itertools.chain(
        balance_tasks,
        sorted(
            retrieve_tasks(
                token=token,
                labels=label_set,
            ),
            key=operator.attrgetter('time'),
        )
    )

    tasks = calculate(tasks)

    print_report(tasks)


if __name__ == '__main__':
    app()
