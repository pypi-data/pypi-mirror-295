def add(a, b):
    """Сложение двух чисел."""
    return a + b

def subtract(a, b):
    """Вычитание второго числа из первого."""
    return a - b

def multiply(a, b):
    """Умножение двух чисел."""
    return a * b

def divide(a, b):
    """Деление первого числа на второе."""
    if b == 0:
        raise ValueError("Делить на ноль нельзя.")
    return a / b
