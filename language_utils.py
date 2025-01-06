import re
import math
from typing import Dict


class LanguageUtils:
    """
    A utility class for converting natural language math expressions into mathematical expressions.
    """

    def __init__(self):
        self.math_keywords = [
            "plus", "minus", "times", "divided by", "log of", "sqrt of",
            "sin of", "cos of", "tan of", "power", "factorial",
            "absolute value", "square root", "sine", "cosine", "tangent"
        ]
        self.remove_phrases_pattern = re.compile(
            r'\b(what is|calculate|the|of|please|compute|find|value|result)\b',
            re.IGNORECASE
        )
        self.remove_chars_pattern = re.compile(r'[?.,!]', re.IGNORECASE)
        self.angle_pattern = re.compile(r'([-0-9.]+)\s*degrees', re.IGNORECASE)
        self.number_pattern = re.compile(r'^[-0-9.]+$', re.IGNORECASE)
        self.functions_patterns: Dict[str, str] = {
            "square root": r'\bsquare root\s*([-\d.]+)\b',
            "log": r'\blog\s*([-\d.]+)\b',
            "sqrt": r'\bsqrt\s*([-\d.]+)\b',
            "sin": r'\bsin(e)?\s*([-\d.]+)\b',
            "cos": r'\bcos(ine)?\s*([-\d.]+)\b',
            "tan": r'\btan(gent)?\s*([-\d.]+)\b',
            "factorial": r'\bfactorial\s*(\d+)\b',
            "absolute": r'\babsolute\s*([-\d.]+)\b',
            "absolute value": r'\babsolute value\s*([-\d.]+)\b',
            "power": r'\bpower\b',
            "to the power of": r'\bto the power of\b'
        }

    def is_math_question(self, text: str) -> bool:
        """
        Checks if the input is a math-related question.

        Args:
            text (str): The input text to check.

        Returns:
            bool: True if the input is a math-related question, otherwise False.
        """
        text = text.lower()
        print(f"Checking if '{text}' is a math question...")
        return any(keyword in text for keyword in self.math_keywords)

    def convert_to_radians(self, angle: str) -> float:
        """
        Converts an angle from degrees to radians if "degrees" is present in the input.
        Otherwise, assumes the angle is already in radians.

        Args:
            angle (str): The angle value as a string.

        Returns:
            float: The angle value in radians.

        Raises:
            ValueError: If the angle cannot be converted to a numeric value.
        """
        match = self.angle_pattern.search(angle)
        if match:
            angle_value = match.group(1)
            try:
                angle_value = float(angle_value)
            except ValueError:
                raise ValueError(
                    f"Angle value '{angle_value}' cannot be converted to a float."
                )
            print(f"Converted '{angle}' to radians: {math.radians(angle_value)}")
            return math.radians(angle_value)
        else:
            try:
                angle_value = float(angle)
            except ValueError:
                raise ValueError(
                    f"Angle value '{angle}' cannot be converted to a float."
                )
            print(f"Assuming '{angle}' is already in radians: {angle_value}")
            return angle_value

    def extract_angle(self, text: str) -> str:
        """
        Extracts the angle value from the input text.

        Args:
            text (str): The input text to extract the angle from.

        Returns:
            str: The extracted angle value.
        """
        words = text.split()
        for i, word in enumerate(words):
            if word in ["sin", "cos", "tan", "cosine", "sine", "tangent"]:
                return ' '.join(words[i + 1:])  # Return the angle value

    def convert_to_math(self, text: str) -> str:
        """
        Converts natural language math expressions into mathematical expressions.

        Args:
            text (str): The input text to convert.

        Returns:
            str: The converted mathematical expression.

        Raises:
            ValueError: If the input cannot be converted to a valid math expression.
        """
        try:
            text = text.lower()
            print(f"Original text: '{text}'")
            # Remove non-math phrases and characters
            text = self.remove_phrases_pattern.sub('', text)
            text = self.remove_chars_pattern.sub('', text)
            print(f"After removing phrases and characters: '{text}'")
            # Replace natural language terms with math operations
            text = text.replace("plus", "+")
            text = text.replace("minus", "-")
            text = text.replace("times", "*")
            text = text.replace("divided by", "/")
            text = text.replace("power", "**")
            text = text.replace("sum of", "+")
            text = text.replace("product of", "*")
            print(f"After replacing terms: '{text}'")
            # Handle "to the power of" separately
            text = text.replace("to the power of", "")
            text = text.replace(" ** ", "**")
            # Handle functions like log, sqrt, sin, etc.
            for keyword, pattern in self.functions_patterns.items():
                if keyword in text:
                    if keyword in ["sin", "cos", "tan"]:  # Handle trigonometric functions separately
                        angle = self.extract_angle(text)
                        text = re.sub(
                            pattern, lambda match: self._replace_function(
                                match, keyword, angle), text, flags=re.IGNORECASE
                        )
                    else:
                        text = re.sub(
                            pattern, lambda match: self._replace_function(
                                match, keyword), text, flags=re.IGNORECASE
                        )
            print(f"After handling functions: '{text}'")
            # Handle 'cosine' separately
            if "cosine" in text:
                text = text.replace("cosine", "cos")
                angle = self.extract_angle(text)
                text = f"cos({self.convert_to_radians(angle)})"
            print(f"After handling cosine: '{text}'")
            # Remove 'to' keyword without introducing typos
            text = re.sub(r'\bto\b', '', text)
            print(f"After removing 'to': '{text}'")
            # Remove 'degrees' keyword
            if "degrees" in text:
                text = text.replace("degrees", "")
            print(f"After removing degrees: '{text}'")
            # Handle 'absolute' separately
            if "absolute" in text:
                text = text.replace("absolute", "abs")
                text = text.replace("value", "")
            print(f"After handling absolute: '{text}'")
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            print(f"After removing extra whitespace: '{text}'")
            # Strip any leading/trailing whitespace
            text = text.strip()
            print(f"After stripping: '{text}'")
            # Validate the final expression
            if not text:
                raise ValueError(
                    "Empty math expression after conversion. Check the input for unsupported phrases."
                )
            # Check if the expression is valid
            try:
                eval(
                    text,
                    {"__builtins__": None},
                    {"sqrt": math.sqrt, "log": math.log, "sin": math.sin,
                     "cos": math.cos, "tan": math.tan, "math": math, "abs": abs}
                )
            except Exception as e:
                raise ValueError(
                    f"Invalid math expression after conversion: '{text}'. Error: {e}"
                )
            return text
        except Exception as e:
            raise ValueError(
                f"Error converting natural language to math expression: {e}. Input: '{text}'"
            )

    def _replace_function(self, match: re.Match, keyword: str, angle: str = None) -> str:
        """
        Replaces a natural language function with its corresponding mathematical expression.

        Args:
            match (re.Match): The regex match object.
            keyword (str): The function keyword (e.g., "sin", "cos", "factorial").
            angle (str, optional): The angle value for trigonometric functions. Defaults to None.

        Returns:
            str: The converted mathematical expression.
        """
        if angle is not None:  # Handle trigonometric functions
            arg = angle
            if keyword in ["sin", "cos", "tan"]:
                arg = self.convert_to_radians(arg)
            result = f"{keyword}({arg})"
            # Fix: Remove 'degrees' keyword from the original match
            text_without_degrees = match.group(0).replace("degrees", "")
            print(f"Replaced '{text_without_degrees}' with '{result}'")
            return result
        else:
            arg = match.group(1) if match.groups() else ""
            if keyword == "square root":
                result = f"sqrt({arg})"
                print(f"Replaced '{match.group(0)}' with '{result}'")
                return result
            elif keyword == "factorial":
                result = f"math.factorial({arg})"
                print(f"Replaced '{match.group(0)}' with '{result}'")
                return result
            elif keyword in ["absolute", "absolute value"]:
                result = f"abs({arg})"
                print(f"Replaced '{match.group(0)}' with '{result}'")
                return result
            elif keyword in ["power", "to the power of"]:
                result = "**"
                print(f"Replaced '{match.group(0)}' with '{result}'")
                return result
            else:
                result = f"{keyword}({arg})"
                print(f"Replaced '{match.group(0)}' with '{result}'")
                return result


# Test for language_utils.py
if __name__ == "__main__":
    print("Testing language_utils.py...")
    language_utils = LanguageUtils()
    # Test is_math_question
    print("Testing is_math_question...")
    assert language_utils.is_math_question("What is 5 plus 5?") == True
    assert language_utils.is_math_question("Tell me a joke") == False
    # Test convert_to_math
    print("\nTesting convert_to_math...")
    assert language_utils.convert_to_math("What is 5 plus 5?") == "5 + 5"
    assert language_utils.convert_to_math(
        "Calculate the square root of 25") == "sqrt(25)"
    assert language_utils.convert_to_math(
        "What is 5 to the power of 3?") == "5 ** 3"
    assert language_utils.convert_to_math(
        "What is the factorial of 5?") == "math.factorial(5)"
    assert language_utils.convert_to_math(
        "What is the absolute value of -7?") == "abs(-7)"
    assert language_utils.convert_to_math(
        "What is the cosine of 60 degrees?") == f"cos({math.radians(60)})"
    # Test convert_to_radians
    print("\nTesting convert_to_radians...")
    assert math.isclose(
        language_utils.convert_to_radians("45 degrees"),
        math.radians(45)
    )
    assert math.isclose(language_utils.convert_to_radians("1.57"), 1.57)
    print("All tests passed!")
