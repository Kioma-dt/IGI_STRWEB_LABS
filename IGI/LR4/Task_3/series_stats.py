import statistics

class SeriesStats:
    """Class To Get Series Statistics"""
    def __init__(self, series: list[float]):
        self.series = series

    @property
    def mean(self):
        """Mean of Series Elements"""
        return statistics.mean(self.series)

    @property
    def mode(self):
        """Mode of Series Elements"""
        return statistics.mode(self.series)
    
    @property
    def median(self):
        """Median of Series Elements"""
        return statistics.median(self.series)
    
    @property
    def variance(self):
        """Variance of Series Elements"""
        return statistics.variance(self.series)
    
    @property
    def stdev(self):
        """Standard Division of Series Elements"""
        return statistics.stdev(self.series)
    
    def __str__(self):
        return f"""Mean: {self.mean}
Mode: {self.mode}
Median: {self.median}
Variance: {self.variance}
Standard Division: {self.stdev}
"""