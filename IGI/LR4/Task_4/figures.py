from abc import abstractmethod, ABC
from color import Color
import matplotlib.pyplot as plt

class Figure(ABC):
    """Abstract Figure Class"""
    _name = "Figure"

    @abstractmethod
    def area(self):
        """Find Area of Figure"""
        pass

    @abstractmethod
    def draw(self):
        """Draw Figure"""
        pass

    @classmethod
    def get_name(cls):
        """Get Figure Name"""
        return cls._name
    

class IsoscelesTriangle(Figure):
    """Class of Isosceles Triangle"""
    _name = "Isosceles Triangle"

    def __init__(self, a: float, h: float, color: str):
        self.a = a
        self.h = h
        self.color = Color(color)

    def area(self):
        return self.a * self.h / 2
    
    def draw(self):
        x = [-self.a / 2, self.a / 2, 0]
        y = [0, 0, self.h]

        figure, ax = plt.subplots()

        ax.fill(x, y, color=self.color.color)

        ax.set_title(self.get_name())
        ax.grid()

        plt.savefig("triangle.png")
        plt.show()

    def __str__(self):
        return "Figure: {0}, base: {1}, height: {2}, color: {3}, area: {4:.2f}".format(
            self.get_name(), self.a, self.h, self.color.color, self.area()
        )