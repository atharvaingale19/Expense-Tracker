class Menu:

    def __init__(self, service):
        self.service = service

    def display(self):
        while True:
            print("\n===== EXPENSE TRACKER =====")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Search Expenses")
            print("4. Update Expense")
            print("5. Delete Expense")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self.add_expense()

                elif choice == "2":
                    self.view_expenses()

                elif choice == "3":
                    self.search_expenses()

                elif choice == "4":
                    self.update_expense()

                elif choice == "5":
                    self.delete_expense()

                elif choice == "6":
                    print("Goodbye!")
                    break

                else:
                    print("Invalid choice. Please enter 1-6.")

            except ValueError as error:
                print(f"Error: {error}")

            except Exception as error:
                print(f"Unexpected error: {error}")

    def add_expense(self):
        print("\n--- Add Expense ---")

        title = input("Title: ")
        amount = input("Amount: ")
        category = input("Category: ")

        expense = self.service.add_expense(
            title,
            amount,
            category
        )

        print(f"Expense added successfully. ID: {expense.id}")

    def view_expenses(self):
        expenses = self.service.get_all_expenses()

        if not expenses:
            print("No expenses found.")
            return

        print("\n--- Expenses ---")

        for expense in expenses:
            print(
                f"[{expense.id}] "
                f"{expense.title} | "
                f"₹{expense.amount:.2f} | "
                f"{expense.category}"
            )

    def search_expenses(self):
        keyword = input("Enter search keyword: ")

        expenses = self.service.search_expenses(keyword)

        if not expenses:
            print("No matching expenses found.")
            return

        for expense in expenses:
            print(
                f"[{expense.id}] "
                f"{expense.title} | "
                f"₹{expense.amount:.2f} | "
                f"{expense.category}"
            )

    def update_expense(self):
        expense_id = int(input("Enter expense ID: "))

        title = input("New title: ")
        amount = input("New amount: ")
        category = input("New category: ")

        success = self.service.update_expense(
            expense_id,
            title,
            amount,
            category
        )

        if success:
            print("Expense updated successfully.")
        else:
            print("Expense not found.")

    def delete_expense(self):
        expense_id = int(input("Enter expense ID: "))

        success = self.service.delete_expense(expense_id)

        if success:
            print("Expense deleted successfully.")
        else:
            print("Expense not found.")