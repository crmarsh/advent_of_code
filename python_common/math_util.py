from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point2D:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def manhattan_length(self):
        return abs(self.x) + abs(self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y


@dataclass(frozen=True, slots=True)
class Point3D:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def manhattan_length(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


@dataclass(slots=True, unsafe_hash=True)
class Range:
    low: int = 0
    too_high: int = 0

    def expand_to(self, val: int) -> None:
        if self.low < self.too_high:
            self.low = min(self.low, val)
            self.too_high = max(self.too_high, val + 1)
        else:
            self.low = val
            self.too_high = val + 1

    def clear(self) -> None:
        self.low = 0
        self.too_high = 0

    def __len__(self) -> int:
        return self.too_high - self.low

    def __contains__(self, val: int) -> bool:
        return self.low <= val < self.too_high

    def __lt__(self, other) -> bool:
        """
        Defines an ordering on Ranges to just compare the lower bound; probably only makes sense in certain limited cases
        """
        return self.low < other.low

    def __iter__(self):
        for x in range(self.low, self.too_high):
            yield x

    def contains_value(self, val) -> bool:
        return self.low <= val < self.too_high

    def contains_range(self, other):
        return self.low <= other.low < other.too_high <= self.too_high

    def wrap(self, val):
        if val in self:
            return val
        x = (val - self.low) % len(self)
        return self.low + x


@dataclass(slots=True)
class BoundingBox3D:
    x_axis: Range = Range()
    y_axis: Range = Range()
    z_axis: Range = Range()

    def expand_to(self, p: Point3D) -> None:
        self.x_axis.expand_to(p.x)
        self.y_axis.expand_to(p.y)
        self.z_axis.expand_to(p.z)

    def __contains__(self, p: Point3D):
        return p.x in self.x_axis and p.y in self.y_axis and p.z in self.z_axis
