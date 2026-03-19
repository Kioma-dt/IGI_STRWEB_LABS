from typing import Generator, Callable
import random as rnd


def get_float(prompt: str, min : float = None, max : float = None) -> float:
    """
    Get Float Number from User
    
    Args:
        prompt: Message for User
        min: Min Number
        max: Max Number

    Returns:
        float: Float Number
    """

    while True:
        try:
            value = float(input(prompt))

            if min is not None and value <= min:
                raise ValueError(f"Value Must be Greater than {min}")
            
            if max is not None and value >= max:
                raise ValueError(f"Value Must be Less than {max}")

            return value
        except ValueError as error:
            print(f"Invalid Input: {error}") 


def get_yes_or_no(prompt: str) -> bool:
    """
    Get User Answer Yes or No
    
    Args:
        prompt: Message for User

    Returns:
        bool: User Answer
    """

    while True:
        answer = input(prompt).lower()
        if answer == "yes" or answer == "y":
            return True
        
        if answer == "no" or answer == "n":
            return False
        
        print("Wrong Answer! Enter yes(y) or no(n)")


def get_pos_int(prompt: str) -> int:
    """
    Get Positive Integer from User
    
    Args:
        prompt: Message for User

    Returns:
        int: Positive Integer
    """

    while True:
        try:
            value = int(input(prompt))

            if (value <= 0):
                raise ValueError("Value Must be Positive!")

            return value
        
        except ValueError as error:
            print(f"Invalid input: {error}") 


def get_int(prompt : str) -> int:
    """
    Get Integer from User
    
    Args:
        prompt: Message for User

    Returns:
        int: Integer Number
    """

    while True:
        try:
            value = int(input(prompt))
            return value
        
        except ValueError as error:
            print(f"Invalid Input: {error}") 


def get_int_list(prompt : str, stop_number : int = 0) -> list[int]:
    """
    Get List of Integers from User
    
    Args:
        prompt: Message for User
        stop_number: Stop Getting Integers

    Returns:
        list: Integers List
    """

    print(prompt)

    lst = []

    x = get_int("Input Integer Value: ")

    while(x != stop_number):
        lst.append(x)
        x = get_int("Input Integer Value: ")

    return lst


def generator_int_list(size : int, min_value : int = -10, max_value : int = 10) -> Generator[int, None, None]:
    """
    Generate List of Integers
    
    Args:
        size: List Size
        min_value: Minimum Value for List
        max_value: Maximum Value for List

    Yields:
        int: List Element
    """

    for _ in range(size):
        yield rnd.randint(-10, 10)

