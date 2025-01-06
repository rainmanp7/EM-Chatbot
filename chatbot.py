# chatbot.py
from math_utils import MathUtils
from language_utils import LanguageUtils
from snn import SpikingNeuralNetwork
from test_suite import test_cases  # Import the test cases

class ChatBot:
    def __init__(self):
        self.snn = SpikingNeuralNetwork()
        self.math_utils = MathUtils()
        self.language_utils = LanguageUtils()
        self.run_test_suite()  # Run the test suite upon initialization

    def run_test_suite(self):
        """Run the test suite and print the results."""
        print("Running test suite...")
        for test_case in test_cases:
            print(f"\nTest Case: {test_case}")
            response = self.respond(test_case)
            print(response)
        print("\nTest suite completed.")

    def respond(self, user_input: str) -> str:
        """Handle user input: variable assignment, math expression evaluation, or natural language math."""
        try:
            if user_input.strip() == "get_variables":
                return self.get_variables()
            elif '=' in user_input:
                var_name, var_value = user_input.split('=', 1)
                var_name, var_value = var_name.strip(), var_value.strip()
                error = self.math_utils.math_validate.validate_variable_name(var_name)
                if error:
                    raise ValueError(error)
                self.math_utils.set_variable(var_name, float(var_value))
                return f"Bot: Variable '{var_name}' set to {var_value}."
            elif self.language_utils.is_math_question(user_input):
                math_expr = self.language_utils.convert_to_math(user_input)
                print(f"Debug: Converted '{user_input}' to '{math_expr}'")  # Debug print
                # Skip validation for natural language inputs
                result = self.math_utils._parse_and_evaluate_expression(math_expr)
                # Suggest optimizations using the SNN
                optimized_expr = self.snn.analyze_expression(math_expr)
                if optimized_expr:
                    return f"Bot: The result is {result}. Suggested optimization: {optimized_expr}"
                else:
                    return f"Bot: The result is {result}."
            elif 'd/dx' in user_input or 'integrate' in user_input:
                return self.math_utils.evaluate_calculus(user_input)
            elif 'det' in user_input or 'inv' in user_input:
                return self.math_utils.evaluate_linear_algebra(user_input)
            else:
                error = self.math_utils.math_validate.validate_math_expression(user_input)
                if error:
                    raise ValueError(error)
                result = self.math_utils._parse_and_evaluate_expression(user_input)
                # Suggest optimizations using the SNN
                optimized_expr = self.snn.analyze_expression(user_input)
                if optimized_expr:
                    return f"Bot: The result is {result}. Suggested optimization: {optimized_expr}"
                else:
                    return f"Bot: The result is {result}."
        except (ValueError, ZeroDivisionError, SyntaxError, NameError, Exception) as e:
            return f"Bot: Error - {e}"

    def get_variables(self) -> str:
        """Return a formatted string of currently defined variables."""
        variables = self.math_utils.get_variables()
        if not variables:
            return "Bot: No variables defined."
        var_string = "Bot: Defined Variables:\n"
        for var, value in variables.items():
            var_string += f"- {var}: {value}\n"
        return var_string

# Main entry point to run the chatbot
if __name__ == "__main__":
    chatbot = ChatBot()  # This will automatically run the test suite