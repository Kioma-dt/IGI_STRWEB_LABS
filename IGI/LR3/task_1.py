"""
Program to Calculate ln((x + 1) / (x - 1)) with Macloren Series
Lab Work 3
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 18-03-2026
"""

import user_input
import math
from typing import Generator, Callable
from os import system


def series_generator(x : float, max_series_len : int) -> Generator[float, None, None]:
    """
    Generate Macloren Series for Function ln((x + 1) / (x - 1))
    
    Args:
        x: Function Argument
        max_series_len: Maximum Series Length

    Yields:
        float: Series
    """

    for n in range(0, max_series_len):
        yield 2 * (1 / (2 * n + 1) / math.pow(x, 2 * n + 1))


def calculation_checker(func : Callable) -> Callable:
    """
    Decorator to Check that abs(x) > 1.
    """
    def wrapper(x, *args, **kwargs):
        if math.fabs(x <= 1):
            raise ValueError(f"Function Argument Module Must be Greater then 1 (abs(x) > 1)!")
        
        return func(x, *args, **kwargs)
    
    return wrapper


@calculation_checker
def calculate(x : float, eps : float, max_iterations : int) -> tuple[float, int]:
    
    """
    Calculate Function ln((x + 1) / (x - 1)) with Macloren Series
    
    Args:
        x: Function Argument
        eps: Precision
        max_iterations: Maximum Iterations

    Returns:
        tuple: [result, iterations]

    Raises:
        ValueError: Not Converged
    """

    result = 0
    iteration = 0

    for iteration, series in enumerate(series_generator(x, max_iterations), 1):
        result += series

        if math.fabs(series) < eps:
            break

    if iteration >= max_iterations:
        raise ValueError(f"Series didn't Converged for {max_iterations} Iterations")
    
    return (result, iteration)


def print_results(x : float, eps : float, math_res : float, results : tuple[float, int]) -> None:
    """
    Print Results Table
    
    Args:
        x: Function Argument
        eps: Precision
        math_res: Calculated Result
        results: [result, iterations]

    """

    result, n = results

    print("\nResults:")
    print("+-----------+-----------+-----------+-----------+-----------+")
    print("|     x     |     n     |   F(x)    | Math F(x) |    eps    |")
    print("+-----------+-----------+-----------+-----------+-----------+")
    print(f"| {x:9.6f} | {n:9d} | {result:9.6f} | {math_res:9.6f} | {eps:9.6f} |")
    print("+-----------+-----------+-----------+-----------+-----------+")


def menu() -> None:
    """
    Menu for Task_1
    """
    
    while True:
        try:
            system("clear")

            print("Program to Calculate ln((x + 1) / (x - 1)) with Macloren Series")
            print("Lab Work 3")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 18-03-2026")
            print()

            # Get user input
            x = user_input.get_float("Enter Function Argument: ")
            eps = user_input.get_float("Enter Precision (eps > 0): ", 0)
            
            # Calculate
            results = calculate(x, eps, 500)
            math_result = math.log((x + 1) / (x - 1))

            # Results
            print_results(x, eps, math_result, results)      

        except ValueError as e:
            print(f"Value Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if not user_input.get_yes_or_no("\nWould You Like to Try Again? (yes / no)"):
                break
        

# If module is executing run it
if __name__ == "__main__":
    menu()


