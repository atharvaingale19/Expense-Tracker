from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService
from app.cli.menu import Menu


def main():
    repository = ExpenseRepository()
    service = ExpenseService(repository)
    menu = Menu(service)

    menu.display()


if __name__ == "__main__":
    main()