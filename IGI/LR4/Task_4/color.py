import matplotlib.colors as mcolors
class Color:
    """Class To Store Color of Figure"""
    def __init__(self, color: str):
        self.color = color

    @property
    def color(self):
        """Figure Color Getter"""
        return self._color

    @color.setter
    def color(self, value: str):
        """Figure Color Setter"""
        try:
            if not value :
                raise ValueError()
            mcolors.to_rgba(value)
            self._color = value
        except ValueError:
            raise ValueError("No Such Color!")
