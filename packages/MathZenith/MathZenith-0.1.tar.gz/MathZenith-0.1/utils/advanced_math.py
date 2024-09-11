# advanced_math.py

import math

def sqrt(x):
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number")
    return math.sqrt(x)

def log(x, base=math.e):
    if x <= 0:
        raise ValueError("Logarithm only defined for positive numbers")
    return math.log(x, base)

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def tan(x):
    return math.tan(x)

def exp(x):
    return math.exp(x)
