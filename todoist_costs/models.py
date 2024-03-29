from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from currency_converter import CurrencyConverter


class TaskType(Enum):
    """Task types."""

    COST = 1
    INCOME = 2


@dataclass
class LabelSet:
    """IDs for the labels we use in the program logic."""

    cost: int
    income: int


@dataclass
class FinancialTask:
    """Todoist task recognized as finanical transaction."""

    name: str
    description: str
    time: Optional[datetime]
    amount: int
    currency: str
    balance: int = 0

    @property
    def is_income(self):
        return self.amount >= 0

    @property
    def standardized_amount(self) -> float:
        if self.currency == 'AMD':
            return self.amount / 383.0

        if self.currency == 'MDL':
            return self.amount / 17.1

        return CurrencyConverter().convert(
            self.amount,
            currency=self.currency,
            new_currency='USD',
        )
