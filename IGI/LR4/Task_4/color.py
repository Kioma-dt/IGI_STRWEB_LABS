import matplotlib.colors as mcolors
class Color:
    def __init__(self, color: str):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        try:
            if not value :
                raise ValueError()
            mcolors.to_rgba(value)
            self._color = value
        except ValueError:
            raise ValueError("Wrong Color!")
