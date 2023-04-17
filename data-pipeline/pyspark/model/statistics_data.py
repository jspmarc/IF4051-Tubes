class StatisticsData(object):
    min: float
    max: float
    mean: float
    median: float
    count: int
    count_unique: int

    def __init__(
        self,
        min: float = 0.0,
        max: float = 0.0,
        mean: float = 0.0,
        median: float = 0.0,
        count: int = 0,
        count_unique: int = 0,
    ):
        self.min = min
        self.max = max
        self.mean = mean
        self.median = median
        self.count = count
        self.count_unique = count_unique

    def __str__(self):
        return f"Count Unique: {self.count_unique}, Count: {self.count}, Max: {self.max}, \
Min: {self.min}, Mean: {self.mean}, Median: {self.median}"
