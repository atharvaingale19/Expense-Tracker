def validate_title(title):
    if not title.strip():
        raise ValueError("Title cannot be empty.")

    if len(title.strip()) > 100:
        raise ValueError("Title cannot exceed 100 characters.")

    return title.strip()


def validate_amount(amount):
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    return amount


def validate_category(category):
    if not category.strip():
        raise ValueError("Category cannot be empty.")

    return category.strip()