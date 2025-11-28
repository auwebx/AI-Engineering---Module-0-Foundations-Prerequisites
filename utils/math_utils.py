from typing import List

# This function takes two integers (a and b) and returns their sum.
# It demonstrates a simple type-hinted arithmetic function.
def add(a: int, b: int) -> int:
    return a + b


# This function multiplies two floating-point numbers (a and b).
# Type hints help ensure callers pass the correct value types.
def multiply(a: float, b: float) -> float:
    return a * b


class Calculator:
    # The constructor initializes a Calculator object.
    # 'name' is an optional argument with a default value "FastAPICalc".
    # 'history' is a list that will store operation records as strings.
    def __init__(self, name: str = "FastAPICalc"):
        self.name = name
        self.history: List[str] = []  # Stores past calculations as readable strings

    # This method adds two integers, records the operation, and returns the result.
    # It stores results in a readable format like "3 + 4 = 7".
    def add_and_record(self, a: int, b: int) -> int:
        result = a + b  # Perform addition
        # Save this calculation to the history list for later reference
        self.history.append(f"{a} + {b} = {result}")
        return result  # Return the computed value

    # This method simply returns the entire history list.
    # Useful for displaying or logging all previous operations.
    def get_history(self) -> List[str]:
        return self.history
