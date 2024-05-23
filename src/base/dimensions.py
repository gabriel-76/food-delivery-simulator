class Dimensions:
    def __init__(self, length, height, width, weight):
        self.length = length
        self.height = height
        self.width = width
        self.weight = weight

    def __lt__(self, other):
        return (
                self.length < other.length and
                self.height < other.height and
                self.width < other.width and
                self.weight < other.weight
        )

    def __gt__(self, other):
        return (
                self.length > other.length and
                self.height > other.height and
                self.width > other.width and
                self.weight > other.weight
        )

    def __eq__(self, other):
        return (
                self.length == other.length and
                self.height == other.height and
                self.width == other.width and
                self.weight == other.weight
        )

    def __add__(self, other):
        return Dimensions(
            self.length + other.length,
            self.height + other.height,
            self.width + other.width,
            self.weight + other.weight
        )
