import math
import matplotlib.pyplot as plt
from typing import Generator, Callable
from series import Series

class Graph:
    @staticmethod
    def draw(function: Callable, series_func: Callable, x_start: float, x_end: float, step: float, eps: float, max_iter: int):
        series = Series(function, series_func)

        x_values = []
        series_values = []
        math_values = []

        x = x_start
        while x <= x_end:
            x_values.append(x)
            series_values.append(series.calculate(x, eps, max_iter)[0])
            math_values.append(function(x))
            x += step

        fig, ax = plt.subplots()

        ax.plot(x_values, series_values, 'red', label="Series F(x)")
        ax.plot(x_values, math_values, 'blue', label="Math F(x)")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Series vs Math")

        ax.annotate("Approaching Infinity",
             xy=(1, function(1.01)),
             xytext=(1.1, 4),
             arrowprops=dict(facecolor="black", shrink=0.01))

        ax.text(3, 1, "Graphics Are Close Enough")

        ax.legend()

        ax.grid(True)

        plt.savefig("plot.png")

        plt.show()

    @staticmethod
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


