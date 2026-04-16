from typing import Generator, Callable
import math

def calculation_checker(func : Callable) -> Callable:
        """
        Decorator to Check that abs(x) > 1.
        """
        def wrapper(self, x, *args, **kwargs):
            if math.fabs(x <= 1):
                raise ValueError(f"Function Argument Module Must be Greater then 1 (abs(x) > 1)!")
            
            return func(self, x, *args, **kwargs)
        
        return wrapper

class Series:
    def __init__(self, function: Callable, series: Callable):
        self.function = function
        self.series = series

    def series_generator(self, x : float, max_series_len : int) -> Generator[float, None, None]:
        """
        Generate Macloren Series for Function ln((x + 1) / (x - 1))
        
        Args:
            x: Function Argument
            max_series_len: Maximum Series Length

        Yields:
            float: Series
        """

        for n in range(0, max_series_len):
            # yield 
            yield self.series(n, x)



    @calculation_checker
    def calculate(self, x : float, eps : float, max_iterations : int) -> tuple[float, int]:
        
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

        for iteration, series_n in enumerate(self.series_generator(x, max_iterations), 1):
            result += series_n

            if math.fabs(series_n) < eps:
                break

        if iteration >= max_iterations:
            raise ValueError(f"Series didn't Converged for {max_iterations} Iterations")
        
        return (result, iteration)
    


    
