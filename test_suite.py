# test_suite.py
# Test cases for the chatbot
test_cases = [
    # Basic arithmetic
    "5 * 6",
    "12 - 7",
    "2^e",
    "sqrt(56)",
    
    # Variable assignments
    "x = 10",
    "x + 7",
    "valid_var = 5",
    
    # Natural language math questions
    "What is 5 plus 5?",
    "Calculate the log of 100.",
    "What is the square root of 25?",
    "Calculate the sine of 90 degrees.",
    "What is 5 to the power of 3?",
    
    # Error cases
    "5+",  # Incomplete expression
    "sqrt(abcd)",  # Undefined variable
    "y + 10",  # Undefined variable
    
    # Calculus operations
    "d/dx(x^2 + 3x)",
    "integrate(x^2 + 3x, x)",
    
    # Linear algebra operations
    "det([[1, 2], [3, 4]])",
    "inv([[1, 2], [3, 4]])",
    
    # Get variables
    "get_variables",
    
    # Complex expressions
    "(5 + 3) * 4",
    "log(5)",
    "5 / 0",  # Division by zero
    "sin(90)",

    # New test cases for enhanced SNN optimizations
    "sin(90) + sin(90)",  # Should suggest 2 * sin(90)
    "log(100) + log(100)",  # Should suggest 2 * log(100)
    "5 + 5 + 5",  # Should suggest 5 * 3
    "2 * 2 * 2",  # Should suggest 2 ^ 3

    # New test cases for natural language math support
    "What is 10 minus 3?",
    "Calculate the square root of 64.",
    "What is the factorial of 5?",
    "What is the absolute value of -7?",
    "What is 2 times 3?",
    "What is 10 divided by 2?",
    "What is the cosine of 60 degrees?",
    "What is the tangent of 45 degrees?",

    # New test cases for higher math operations
    "d/dx(sin(x))",  # Derivative of sin(x)
    "integrate(cos(x), x)",  # Integral of cos(x)
    "det([[2, 0], [0, 2]])",  # Determinant of a 2x2 matrix
    "inv([[2, 0], [0, 2]])",  # Inverse of a 2x2 matrix
]

# Test for test_suite.py
if __name__ == "__main__":
    print("Testing test_suite.py...")
    print("Number of test cases:", len(test_cases))
    print("First test case:", test_cases[0])
    print("Last test case:", test_cases[-1])
    print("All test cases loaded successfully!")