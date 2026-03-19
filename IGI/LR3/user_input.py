from typing import Generator, Callable
import random as rnd


def repeat_input (func : Callable) -> Callable:
    """
    Decorator to Repeat Input Request if It Was Incorrect
    """

    def wrapper(*args, **kwargs):
        while True:
            try:
                val = func(*args, **kwargs)

                return val
            
            except ValueError as error:
                print(f"Invalid Input: {error}") 

            except Exception as error:
                print(f"Error: {error}")

    return wrapper


@repeat_input
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

    value = float(input(prompt))

    if min is not None and value <= min:
        raise ValueError(f"Value Must be Greater than {min}")
            
    if max is not None and value >= max:
        raise ValueError(f"Value Must be Less than {max}")

    return value


@repeat_input
def get_yes_or_no(prompt: str) -> bool:
    """
    Get User Answer Yes or No
    
    Args:
        prompt: Message for User

    Returns:
        bool: User Answer
    """

    answer = input(prompt).lower()
    if answer == "yes" or answer == "y":
        return True
        
    if answer == "no" or answer == "n":
        return False
        
    raise ValueError("Wrong Answer! Enter yes(y) or no(n)")


@repeat_input
def get_pos_int(prompt: str,  min : int = None, max : int = None) -> int:
    """
    Get Positive Integer from User
    
    Args:
        prompt: Message for User

    Returns:
        int: Positive Integer
    """

    value = int(input(prompt))

    if min is not None and value <= min:
        raise ValueError(f"Value Must be Greater than {min}")
            
    if max is not None and value >= max:
        raise ValueError(f"Value Must be Less than {max}")


    if (value <= 0):
        raise ValueError("Value Must be Positive!")

    return value


@repeat_input
def get_int(prompt : str,  min : int = None, max : int = None) -> int:
    """
    Get Integer from User
    
    Args:
        prompt: Message for User

    Returns:
        int: Integer Number
    """

    value = int(input(prompt))

    if min is not None and value <= min:
        raise ValueError(f"Value Must be Greater than {min}")
            
    if max is not None and value >= max:
        raise ValueError(f"Value Must be Less than {max}")

    return value


@repeat_input
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

@repeat_input
def get_float_list(prompt : str, list_size : int) -> list[float]:
    """
    Get List of Float Numbers from User
    
    Args:
        prompt: Message for User
        list_size: Size of the List

    Returns:
        list: Float List
    """

    print(prompt)

    lst = []

    for x in range(list_size):
        x = get_float("Input Float Value: ")
        lst.append(x)

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
        yield rnd.randint(min_value, max_value)

def generator_float_list(size : int, min_value : float = -10, max_value : float = 10) -> Generator[float, None, None]:
    """
    Generate List of Float Numbers
    
    Args:
        size: List Size
        min_value: Minimum Value for List
        max_value: Maximum Value for List

    Yields:
        float: List Element
    """

    for _ in range(size):
        yield rnd.uniform(min_value, max_value)


