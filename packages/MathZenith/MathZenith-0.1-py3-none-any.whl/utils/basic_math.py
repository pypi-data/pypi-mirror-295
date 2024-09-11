# basic_math.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

def power(base, exp):
    return base ** exp
