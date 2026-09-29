import streamlit as st
from collections import Counter

from app.services.expense_service import ExpenseService
from app.repositories.expense_repository import ExpenseRepository


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# ---------------------------------------------------------
# Initialize application services
# ---------------------------------------------------------

@st.cache_resource
def get_service():
    repository = ExpenseRepository()
    return ExpenseService(repository)


service = get_service()


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def get_expenses():
    """Return all expenses from the service."""
    return service.get_all_expenses()


def expense_to_dict(expense):
    """Convert an Expense object into a dictionary for display."""
    return {
        "ID": expense.id,
        "Title": expense.title,
        "Amount": expense.amount,
        "Category": expense.category
    }


def refresh():
    """Trigger a Streamlit rerun after a data-changing operation."""
    st.rerun()


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------

st.sidebar.title("💰 Expense Tracker")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Expense",
        "View Expenses",
        "Search Expenses",
        "Update Expense",
        "Delete Expense"
    ]
)


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

if page == "Dashboard":

    st.title("💰 Expense Tracker")
    st.caption("Simple expense management with persistent JSON storage.")

    expenses = get_expenses()

    total_spending = sum(expense.amount for expense in expenses)
    expense_count = len(expenses)

    categories = Counter(
        expense.category for expense in expenses
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Spending",
            f"₹{total_spending:,.2f}"
        )

    with col2:
        st.metric(
            "Total Expenses",
            expense_count
        )

    with col3:
        st.metric(
            "Categories",
            len(categories)
        )

    st.divider()

    if not expenses:
        st.info("No expenses recorded yet.")
    else:
        st.subheader("Category Summary")

        category_rows = [
            {
                "Category": category,
                "Number of Expenses": count,
                "Total Amount": sum(
                    expense.amount
                    for expense in expenses
                    if expense.category == category
                )
            }
            for category, count in categories.items()
        ]

        st.dataframe(
            category_rows,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Recent Expenses")

        recent_expenses = [
            expense_to_dict(expense)
            for expense in expenses[-5:]
        ]

        st.dataframe(
            recent_expenses,
            use_container_width=True,
            hide_index=True
        )


# ---------------------------------------------------------
# Add Expense
# ---------------------------------------------------------

elif page == "Add Expense":

    st.title("➕ Add Expense")

    with st.form("add_expense_form"):

        title = st.text_input(
            "Expense Title",
            placeholder="e.g. Lunch"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=1.0,
            format="%.2f"
        )

        category = st.text_input(
            "Category",
            placeholder="e.g. Food"
        )

        submitted = st.form_submit_button(
            "Add Expense",
            use_container_width=True
        )

    if submitted:

        try:
            expense = service.add_expense(
                title=title,
                amount=amount,
                category=category
            )

            st.success(
                f"Expense #{expense.id} added successfully."
            )

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                f"An unexpected error occurred: {error}"
            )


# ---------------------------------------------------------
# View Expenses
# ---------------------------------------------------------

elif page == "View Expenses":

    st.title("📋 All Expenses")

    expenses = get_expenses()

    if not expenses:
        st.info("No expenses found.")
    else:

        rows = [
            expense_to_dict(expense)
            for expense in expenses
        ]

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

        total = sum(expense.amount for expense in expenses)

        st.metric(
            "Total Spending",
            f"₹{total:,.2f}"
        )


# ---------------------------------------------------------
# Search Expenses
# ---------------------------------------------------------

elif page == "Search Expenses":

    st.title("🔎 Search Expenses")

    keyword = st.text_input(
        "Search by title or category",
        placeholder="e.g. food"
    )

    if keyword.strip():

        try:
            results = service.search_expenses(keyword)

            if not results:
                st.warning("No matching expenses found.")
            else:

                rows = [
                    expense_to_dict(expense)
                    for expense in results
                ]

                st.dataframe(
                    rows,
                    use_container_width=True,
                    hide_index=True
                )

                st.success(
                    f"{len(results)} matching expense(s) found."
                )

        except Exception as error:
            st.error(
                f"An unexpected error occurred: {error}"
            )


# ---------------------------------------------------------
# Update Expense
# ---------------------------------------------------------

elif page == "Update Expense":

    st.title("✏️ Update Expense")

    expenses = get_expenses()

    if not expenses:

        st.info("No expenses available to update.")

    else:

        expense_options = {
            f"#{expense.id} - {expense.title}": expense.id
            for expense in expenses
        }

        selected_label = st.selectbox(
            "Select an expense",
            list(expense_options.keys())
        )

        selected_id = expense_options[selected_label]

        selected_expense = next(
            expense
            for expense in expenses
            if expense.id == selected_id
        )

        st.divider()

        with st.form("update_expense_form"):

            title = st.text_input(
                "Expense Title",
                value=selected_expense.title
            )

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=float(selected_expense.amount),
                step=1.0,
                format="%.2f"
            )

            category = st.text_input(
                "Category",
                value=selected_expense.category
            )

            submitted = st.form_submit_button(
                "Update Expense",
                use_container_width=True
            )

        if submitted:

            try:

                updated = service.update_expense(
                    expense_id=selected_id,
                    title=title,
                    amount=amount,
                    category=category
                )

                if updated:
                    st.success(
                        f"Expense #{selected_id} updated successfully."
                    )
                    st.rerun()
                else:
                    st.error(
                        "Expense could not be found."
                    )

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(
                    f"An unexpected error occurred: {error}"
                )


# ---------------------------------------------------------
# Delete Expense
# ---------------------------------------------------------

elif page == "Delete Expense":

    st.title("🗑️ Delete Expense")

    expenses = get_expenses()

    if not expenses:

        st.info("No expenses available to delete.")

    else:

        expense_options = {
            f"#{expense.id} - {expense.title} - ₹{expense.amount:.2f}":
                expense.id
            for expense in expenses
        }

        selected_label = st.selectbox(
            "Select an expense",
            list(expense_options.keys())
        )

        selected_id = expense_options[selected_label]

        st.warning(
            "Deleting an expense permanently removes it from the JSON storage."
        )

        if st.button(
            "Delete Expense",
            type="primary",
            use_container_width=True
        ):

            try:

                deleted = service.delete_expense(
                    selected_id
                )

                if deleted:
                    st.success(
                        f"Expense #{selected_id} deleted successfully."
                    )
                    st.rerun()
                else:
                    st.error(
                        "Expense could not be found."
                    )

            except Exception as error:
                st.error(
                    f"An unexpected error occurred: {error}"
                )