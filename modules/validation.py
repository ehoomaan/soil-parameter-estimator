def validate_positive(value: float, name: str) -> str | None:
    """
    Return an error message if value is not positive.
    Otherwise return None.
    """
    if value <= 0:
        return f"{name} must be greater than zero."
    return None


def validate_nonnegative(value: float, name: str) -> str | None:
    """
    Return an error message if value is negative.
    Otherwise return None.
    """
    if value < 0:
        return f"{name} cannot be negative."
    return None


def validate_correction_factor(value: float, name: str) -> str | None:
    """
    Basic validation for SPT correction factors.
    """
    if value <= 0:
        return f"{name} must be greater than zero."

    if value > 2.0:
        return f"{name} appears unusually high. Please check the input."

    return None
