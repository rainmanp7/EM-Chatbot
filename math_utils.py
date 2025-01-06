# math_utils.py
import re
import math
import numpy as np
import sympy as sp
from math_validate import MathValidate

class MathUtils:
    """
    A utility class for evaluating mathematical expressions with support for variables, 
    common math functions, and basic arithmetic operations.
    """

    def __init__(self):
        """
        Initializes the MathUtils instance with an empty dictionary for variables and 
        predefined supported functions and operations.
        """
        self.variables = {}  # Initialize an empty dictionary for variables
        self.supported_functions = {
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e,
            'factorial': math.factorial,
            'abs': abs,
            'exp': math.exp,
            'radians': math.radians
        }
        self.supported_operations = ['+', '-', '*', '/', '^']
        self.math_validate = MathValidate(self.supported_functions, self.supported_operations, self.variables) 

    def set_variable(self, var_name: str, var_value: float) -> None:
        """
        Sets a variable to a specific value.

        Args:
            var_name (str): The name of the variable.
            var_value (float): The value of the variable.

        Raises:
            ValueError: If the variable name is invalid.
        """
        error = self.math_validate.validate_variable_name(var_name)
        if error:
            raise ValueError(error)
        self.variables[var_name] = var_value

    def get_variables(self) -> dict:
        """
        Returns a dictionary of currently defined variables.

        Returns:
            dict: A dictionary containing variable names as keys and their values as values.
        """
        return self.variables

    def _parse_and_evaluate_expression(self, expression: str) -> float:
        """
        Replaces supported functions and constants, then evaluates the expression.

        Args:
            expression (str): The math expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If division by zero occurs or an error is encountered during evaluation.
            NameError: If an undefined variable is used in the expression.
            SyntaxError: If the input expression is syntactically incorrect.
        """
        try:
            # Replace natural language terms with math operations
            expression = expression.lower()
            expression = expression.replace("plus", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("times", "*")
            expression = expression.replace("divided by", "/")
            expression = expression.replace("to the power of", "^")
            expression = expression.replace("power", "^")

            # Handle degree-based trigonometric functions
            trig_funcs = ['sin', 'cos', 'tan']
            for func in trig_funcs:
                pattern = rf"{func}\s*of\s*(\d+)\s*degrees"
                match = re.search(pattern, expression)
                if match:
                    value_in_degrees = float(match.group(1))
                    value_in_radians = math.radians(value_in_degrees)
                    expression = expression.replace(match.group(0), f"{func}({value_in_radians})")

            # Replace supported functions and constants
            for func, value in self.supported_functions.items():
                expression = expression.replace(func, f'math.{func}')
            expression = expression.replace('^', '**')
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": None}, {"math": math, **self.variables})
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed.")
        except NameError as e:
            undefined_var = str(e).split("'")[1]  # Extract the undefined variable name
            raise NameError(f"Undefined variable '{undefined_var}'. Please assign a value to it first.")
        except SyntaxError:
            raise SyntaxError("Invalid math expression. Please check your input.")
        except Exception as e:
            raise ValueError(f"Error evaluating math expression: {e}")

    def evaluate_expression(self, expression: str) -> float:
        """
        Evaluates a mathematical expression with support for variables, common math functions, 
        and basic arithmetic operations.

        Args:
            expression (str): The math expression to evaluate.

        Returns:
            float: The result of the evaluated expression.

        Raises:
            ValueError: If the expression is invalid or an error is encountered during evaluation.
        """
        error = self.math_validate.validate_math_expression(expression)
        if error:
            raise ValueError(error)
        return self._parse_and_evaluate_expression(expression)

    def evaluate_calculus(self, expression: str) -> str:
        """
        Evaluates calculus expressions (derivatives and integrals) using SymPy.

        Args:
            expression (str): The calculus expression to evaluate.

        Returns:
            str: The result of the calculus operation.
        """
        try:
            x = sp.symbols('x')
            expression = expression.replace('^', '**')  # Replace ^ with ** for SymPy
            
            if 'd/dx' in expression:
                # Extract the expression to differentiate
                expr = expression.replace('d/dx', '').strip()
                # Ensure the expression is compatible with SymPy
                expr = expr.replace(' ', '')  # Remove spaces
                expr = sp.sympify(expr)  # Parse the expression
                derivative = sp.diff(expr, x)
                return f"Derivative: {derivative}"
            
            elif 'integrate' in expression:
                # Extract the expression to integrate
                expr = expression.replace('integrate', '').strip()
                # Ensure the expression is compatible with SymPy
                expr = expr.replace(' ', '')  # Remove spaces
                expr = sp.sympify(expr)  # Parse the expression
                integral = sp.integrate(expr, x)
                return f"Integral: {integral}"
            
            else:
                return "Invalid calculus expression."
        except Exception as e:
            return f"Error evaluating calculus expression: {e}"

    def evaluate_linear_algebra(self, expression: str) -> str:
        """
        Evaluates linear algebra expressions (matrix operations) using NumPy.

        Args:
            expression (str): The linear algebra expression to evaluate.

        Returns:
            str: The result of the linear algebra operation.
        """
        try:
            if 'det' in expression:
                matrix = eval(expression.replace('det', ''))
                determinant = np.linalg.det(matrix)
                return f"Determinant: {determinant}"
            elif 'inv' in expression:
                matrix = eval(expression.replace('inv', ''))
                inverse = np.linalg.inv(matrix)
                return f"Inverse: {inverse}"
            else:
                return "Invalid linear algebra expression."
        except Exception as e:
            return f"Error evaluating linear algebra expression: {e}"

# Test for math_utils.py
if __name__ == "__main__":
    print("Testing math_utils.py...")
    math_utils = MathUtils()
    
    # Test variable assignment
    math_utils.set_variable("x", 10)
    print("Variable 'x' set to 10.")
    
    # Test evaluate_expression
    print("Evaluating 'x + 5':", math_utils.evaluate_expression("x + 5"))  # 15.0
    
    # Test evaluate_calculus
    print("Evaluating 'd/dx(x^2 + 3x)':", math_utils.evaluate_calculus("d/dx(x^2 + 3x)"))  # Derivative: 2*x + 3
    
    # Test evaluate_linear_algebra
    print("Evaluating 'det([[1, 2], [3, 4]])':", math_utils.evaluate_linear_algebra("det([[1, 2], [3, 4]])"))  # Determinant: -2.0
    
    print("All tests passed!")