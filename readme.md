# Expense Tracker CLI

A command-line expense tracker built with Python. The application allows users to manage their expenses through a menu-driven interface with persistent JSON storage.

## Features

- Add new expenses
- View all expenses
- Update existing expenses
- Delete expenses
- Search expenses by title or category
- Persistent data storage using JSON
- Input validation
- Exception handling
- Modular project structure
- Unit tests for core functionality

## Technologies Used

- Python 3
- JSON
- Git
- GitHub
- Python `dataclasses`
- Python `unittest`

## Project Structure

```text
expense-tracker/
│
├── app/
│   ├── cli/
│   │   └── menu.py
│   │
│   ├── models/
│   │   └── expense.py
│   │
│   ├── repositories/
│   │   └── expense_repository.py
│   │
│   ├── services/
│   │   └── expense_service.py
│   │
│   ├── utils/
│   │   └── validators.py
│   │
│   └── main.py
│
├── data/
│   └── expenses.json
│
├── tests/
│   └── test_expense_service.py
│
├── .gitignore
├── readme.md
└── requirements.txt
