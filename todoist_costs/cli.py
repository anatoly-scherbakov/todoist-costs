import datetime
import itertools
import operator
from typing import List, Optional

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
    days: Optional[int] = Option(default=None, help='Number of days to plan ahead for.'),
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

    retrieved_tasks = sorted(
        retrieve_tasks(
            token=token,
            labels=label_set,
        ),
        key=operator.attrgetter('time'),
    )

    tasks = itertools.chain(
        balance_tasks,
        retrieved_tasks,
    )

    tasks = calculate(tasks)

    if days is not None:
        last_date = datetime.date.today() + datetime.timedelta(days=days)
        tasks = filter(
            lambda task: task.time is None or task.time.date() <= last_date,
            tasks,
        )

    print_report(tasks)


if __name__ == '__main__':
    app()
