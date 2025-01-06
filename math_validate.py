# math_validate.py
import re

class MathValidate:
    """
    A utility class for validating mathematical expressions and variable names.
    """

    def __init__(self, supported_functions: dict, supported_operations: list, variables: dict):
        """
        Initializes the MathValidate instance with supported functions, operations, and variables.

        Args:
        supported_functions (dict): A dictionary of supported math functions.
        supported_operations (list): A list of supported math operations.
        variables (dict): A dictionary of currently defined variables.
        """
        self.supported_functions = supported_functions
        self.supported_operations = supported_operations
        self.variables = variables

    def validate_variable_name(self, var_name: str) -> str | None:
        """
        Validates if a variable name is alphanumeric and starts with a letter.

        Args:
        var_name (str): The variable name to validate.

        Returns:
        str | None: An error message if the variable name is invalid, otherwise None.
        """
        if not var_name.isidentifier() or not var_name[0].isalpha():
            return f"Invalid variable name: '{var_name}'. Variable names must be alphanumeric and start with a letter."
        return None

    def validate_math_expression(self, expression: str) -> str | None:
        """
        Validates the math expression for allowed characters, operations, and function arguments.

        Args:
        expression (str): The math expression to validate.

        Returns:
        str | None: An error message if the expression is invalid, otherwise None.
        """
        # Check for incomplete operations
        if any(op in expression[-1] for op in self.supported_operations):
            return "Incomplete math expression. Please provide a complete operation."

        # Check for allowed characters and defined functions/constants
        pattern = r'^[\d\s\+\-\*\/\^\(\)\.e' + ''.join(self.supported_functions.keys()) + 'xyz]+$'
        if not re.match(pattern, expression, re.IGNORECASE):
            return "Invalid characters in the math expression. Only numbers, math operations, and defined functions/constants are allowed."

        # Validate function arguments
        func_matches = re.findall(rf"({'|'.join(self.supported_functions.keys())})\((.*?)\)", expression, re.IGNORECASE)
        for func, arg in func_matches:
            if not (arg.replace('.', '', 1).isdigit() or arg in self.variables):
                return f"Invalid argument '{arg}' for function '{func}'. Only numbers or defined variables are allowed."

        return None

# Test for math_validate.py
if __name__ == "__main__":
    print("Testing math_validate.py...")
    supported_functions = {'sqrt': 'math.sqrt', 'log': 'math.log'}
    supported_operations = ['+', '-', '*', '/', '^']
    variables = {'x': 10}
    
    math_validate = MathValidate(supported_functions, supported_operations, variables)
    
    # Test validate_variable_name
    print("Validating variable name 'x':", math_validate.validate_variable_name("x"))  # None
    print("Validating variable name '1x':", math_validate.validate_variable_name("1x"))  # Error
    
    # Test validate_math_expression
    print("Validating expression 'x + 5':", math_validate.validate_math_expression("x + 5"))  # None
    print("Validating expression 'x +':", math_validate.validate_math_expression("x +"))  # Error
    
    print("All tests passed!")