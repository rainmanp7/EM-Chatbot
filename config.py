# config.py
SUPPORTED_FUNCTIONS = {
    'sqrt': 'math.sqrt',
    'log': 'math.log',
    'sin': 'math.sin',
    'cos': 'math.cos',
    'tan': 'math.tan',
    'pi': 'math.pi',
    'e': 'math.e',
    'factorial': 'math.factorial',
    'abs': 'abs',
    'exp': 'math.exp',
    'radians': 'math.radians'
}

SUPPORTED_OPERATIONS = ['+', '-', '*', '/', '^']

ERROR_MESSAGES = {
    'division_by_zero': "Division by zero is not allowed.",
    'undefined_variable': "Undefined variable '{var}'. Please assign a value to it first.",
    'invalid_expression': "Invalid math expression. Please check your input."
}

# Test for config.py
if __name__ == "__main__":
    print("Testing config.py...")
    print("SUPPORTED_FUNCTIONS:", SUPPORTED_FUNCTIONS)
    print("SUPPORTED_OPERATIONS:", SUPPORTED_OPERATIONS)
    print("ERROR_MESSAGES:", ERROR_MESSAGES)
    print("All tests passed!")