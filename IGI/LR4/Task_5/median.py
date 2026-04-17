class ManualMedian:
    """Manual Median Calculation"""
    @staticmethod
    def calculate(array) -> float:
        """Calculate Median of Array Manually
        Args:
            array: Processing Array
        Returns:
            float: Median of Array
        """
        sorted_array = sorted(array)
        n = len(sorted_array)

        if n % 2 == 0:
            return (sorted_array[n // 2 - 1] + sorted_array[n // 2]) / 2
        else:
            return sorted_array[n // 2]