from typing import Generator, Callable
import random as rnd

def get_float(prompt: str, min : float = None, max : float = None) -> float:
    """
    Get float number from user
    
    Args:
        prompt: Message for user
        min: Min number
        max: Max number

    Returns:
        float: Float number
    """

    while True:
        try:
            value = float(input(prompt))

            if min is not None and value <= min:
                raise ValueError(f"Value must be greater than {min}")
            if max is not None and value >= max:
                raise ValueError(f"Value must be less than {max}")

            return value
        except ValueError as error:
            print(f"Invalid input: {error}") 


def get_yes_or_no(prompt: str) -> bool:
    """
    Get user answer yes or mo
    
    Args:
        prompt: Message for user

    Returns:
        bool: User answer
    """

    while True:
        answer = input(prompt).lower()
        if answer == "yes" or answer == "y":
            return True
        if answer == "no" or answer == "n":
            return False
        print("Wrong answer! Enter yes(y) or no(n)")

def get_pos_int(prompt: str) -> int:
    """
    Get positive integer from user
    
    Args:
        prompt: Message for user

    Returns:
        int: Positive integer number
    """

    while True:
        try:
            value = int(input(prompt))

            if (value <= 0):
                raise ValueError("Value must be positive!")

            return value
        except ValueError as error:
            print(f"Invalid input: {error}") 

def get_int(prompt : str) -> int:
    """
    Get integer from user
    
    Args:
        prompt: Message for user

    Returns:
        int: Integer number
    """

    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError as error:
            print(f"Invalid input: {error}") 

def get_int_list(prompt : str, stop_number : int = 0) -> list[int]:
    """
    Get list of integers from user
    
    Args:
        prompt: Message for user
        stop_number: Stop getting integers

    Returns:
        list: Integers list
    """

    print(prompt)

    lst = []

    x = get_int("Input integer value: ")

    while(x != stop_number):
        lst.append(x)
        x = get_int("Input integer value: ")

    return lst

def generator_int_list(size : int, min_value : int = -10, max_value : int = 10) -> Generator[int, None, None]:
    """
    Generate list of integers
    
    Args:
        size: List size
        min_value: Minimum value for list
        max_value: Maximum value for list

    Yields:
        int: List element
    """

    for _ in range(size):
        yield rnd.randint(-10, 10)

