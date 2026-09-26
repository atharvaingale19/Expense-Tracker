import json
from pathlib import Path

from app.models.expense import Expense


class ExpenseRepository:

    def __init__(self, file_path="data/expenses.json"):
        self.file_path = Path(file_path)

    def _load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return [Expense.from_dict(item) for item in data]

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            raise ValueError("Storage file contains invalid JSON.")

    def _save(self, expenses):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [expense.to_dict() for expense in expenses],
                file,
                indent=4
            )

    def get_all(self):
        return self._load()

    def get_by_id(self, expense_id):
        expenses = self._load()

        for expense in expenses:
            if expense.id == expense_id:
                return expense

        return None

    def add(self, expense):
        expenses = self._load()
        expenses.append(expense)
        self._save(expenses)

    def update(self, updated_expense):
        expenses = self._load()

        for index, expense in enumerate(expenses):
            if expense.id == updated_expense.id:
                expenses[index] = updated_expense
                self._save(expenses)
                return True

        return False

    def delete(self, expense_id):
        expenses = self._load()

        updated_expenses = [
            expense for expense in expenses
            if expense.id != expense_id
        ]

        if len(updated_expenses) == len(expenses):
            return False

        self._save(updated_expenses)
        return True