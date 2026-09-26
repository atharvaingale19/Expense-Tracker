from app.models.expense import Expense
from app.utils.validators import (
    validate_title,
    validate_amount,
    validate_category
)


class ExpenseService:

    def __init__(self, repository):
        self.repository = repository

    def _generate_id(self):
        expenses = self.repository.get_all()

        if not expenses:
            return 1

        return max(expense.id for expense in expenses) + 1

    def add_expense(self, title, amount, category):
        title = validate_title(title)
        amount = validate_amount(amount)
        category = validate_category(category)

        expense = Expense(
            id=self._generate_id(),
            title=title,
            amount=amount,
            category=category
        )

        self.repository.add(expense)

        return expense

    def get_all_expenses(self):
        return self.repository.get_all()

    def search_expenses(self, keyword):
        keyword = keyword.lower().strip()

        expenses = self.repository.get_all()

        return [
            expense
            for expense in expenses
            if keyword in expense.title.lower()
            or keyword in expense.category.lower()
        ]

    def update_expense(self, expense_id, title, amount, category):
        title = validate_title(title)
        amount = validate_amount(amount)
        category = validate_category(category)

        expense = Expense(
            id=expense_id,
            title=title,
            amount=amount,
            category=category
        )

        return self.repository.update(expense)

    def delete_expense(self, expense_id):
        return self.repository.delete(expense_id)