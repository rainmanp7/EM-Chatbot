import math
import re
from snn import SpikingNeuralNetwork

class ChatBot:
    def __init__(self):
        self.snn = SpikingNeuralNetwork()
        self.variables = {}
        self.supported_functions = {
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        }
        self.supported_operations = ['+', '-', '*', '/', '^']

    def _validate_variable_name(self, var_name: str) -> str | None:
        """Validate if a variable name is alphanumeric and starts with a letter."""
        if not var_name.isidentifier():
            return f"Invalid variable name: '{var_name}'. Variable names must be alphanumeric and start with a letter."
        return None

    def _validate_math_expression(self, expression: str) -> str | None:
        """Validate the math expression for allowed characters, operations, and function arguments."""
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

    def _parse_and_evaluate_expression(self, expression: str) -> float:
        """Replace supported functions and constants, then evaluate the expression."""
        for func, value in self.supported_functions.items():
            expression = expression.replace(func, f'math.{func}')
        expression = expression.replace('^', '**')
        
        try:
            result = eval(expression, {"__builtins__": None}, {"math": math, **self.variables})
            
            # Trigger the SNN to analyze the expression
            self.snn.step([("math_operation", expression)])
            
            # Check if the SNN suggests an optimization
            optimized_expression = self.snn.analyze_expression(expression)
            if optimized_expression and optimized_expression != expression:
                print(f"SNN suggests optimizing: {expression} → {optimized_expression}")
                result = eval(optimized_expression, {"__builtins__": None}, {"math": math, **self.variables})
            
            return result
        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed.")
        except NameError as e:
            raise NameError(f"Undefined variable '{str(e).split(' ')[1]}'. Please assign a value to it first.")
        except SyntaxError:
            raise SyntaxError("Invalid math expression. Please check your input.")
        except Exception as e:
            raise ValueError(f"Error evaluating math expression: {e}")

    def respond(self, user_input: str) -> str:
        """Handle user input: variable assignment or math expression evaluation."""
        try:
            if '=' in user_input:
                var_name, var_value = user_input.split('=', 1)
                var_name, var_value = var_name.strip(), var_value.strip()
                error = self._validate_variable_name(var_name)
                if error:
                    raise ValueError(error)
                self.variables[var_name] = float(var_value)
                return f"Bot: Variable '{var_name}' set to {var_value}."
            error = self._validate_math_expression(user_input)
            if error:
                raise ValueError(error)
            result = self._parse_and_evaluate_expression(user_input)
            return f"Bot: The result is {result}."
        except (ValueError, ZeroDivisionError, SyntaxError, NameError, Exception) as e:
            return f"Bot: Error - {e}"

    def get_variables(self) -> str:
        """Return a formatted string of currently defined variables."""
        if not self.variables:
            return "Bot: No variables defined."
        var_string = "Bot: Defined Variables:\n"
        for var, value in self.variables.items():
            var_string += f"- {var}: {value}\n"
        return var_string

if __name__ == "__main__":
    chatbot = ChatBot()
    
    # Test suite
    test_cases = [
        "5 * 6", "12 - 7", "2^e", "sqrt(56)", 
        "x = 10", "x + 7", "5+", "valid_var = 5", 
        "log(5)", "5 / 0", "sqrt(abcd)", "y + 10", 
        "log(100)", "(5 + 3) * 4", "sin(90)", 
        "get_variables"
    ]
    for case in test_cases:
        print(f"User: {case}")
        if case.lower() == "get_variables":
            print(chatbot.get_variables())
        else:
            print(chatbot.respond(case))
        print("-" * 20)

    # Interactive mode
    print("Entering interactive mode. Type 'exit' or 'quit' to end.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        if user_input.lower() == "get_variables":
            print(chatbot.get_variables())
        else:
            print(chatbot.respond(user_input))