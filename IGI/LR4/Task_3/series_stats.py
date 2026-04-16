import statistics

class SeriesStats:
    def __init__(self, series: list[float]):
        self.series = series

    @property
    def mean(self):
        return statistics.mean(self.series)

    @property
    def mode(self):
        return statistics.mode(self.series)
    
    @property
    def median(self):
        return statistics.median(self.series)
    
    @property
    def variance(self):
        return statistics.variance(self.series)
    
    @property
    def stdev(self):
        return statistics.stdev(self.series)
    
    def __str__(self):
        return f"""Mean: {self.mean}
Mode: {self.mode}
Median: {self.median}
Variance: {self.variance}
Standard Division: {self.stdev}
"""