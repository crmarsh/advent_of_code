from dataclasses import dataclass, field
from typing import Iterator


@dataclass(frozen=True, slots=True)
class Point2D:
    x: int = 0
    y: int = 0

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __add__(self, other: "Point2D") -> "Point2D":
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point2D") -> "Point2D":
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> "Point2D":
        return Point2D(self.x * scalar, self.y * scalar)

    def __floordiv__(self, scalar: int) -> "Point2D":
        return Point2D(self.x // scalar, self.y // scalar)

    def manhattan_length(self) -> int:
        return abs(self.x) + abs(self.y)

    def dot(self, other: "Point2D") -> int:
        return self.x * other.x + self.y * other.y


@dataclass(frozen=True, slots=True)
class Point3D:
    x: int = 0
    y: int = 0
    z: int = 0

    @staticmethod
    def from_p2(other: Point2D, z: int = 0) -> "Point3D":
        return Point3D(other.x, other.y, z)

    def as_p2(self) -> Point2D:
        return Point2D(self.x, self.y)

    def __add__(self, other: "Point3D") -> "Point3D":
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Point3D") -> "Point3D":
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def manhattan_length(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def dot(self, other: "Point3D") -> int:
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

    def __lt__(self, other: "Range") -> bool:
        """
        Defines an ordering on Ranges to just compare the lower bound; probably only makes sense in certain limited cases
        """
        return self.low < other.low

    def __iter__(self) -> Iterator[int]:
        for x in range(self.low, self.too_high):
            yield x

    def contains_value(self, val: int) -> bool:
        return self.low <= val < self.too_high

    def contains_range(self, other: "Range") -> bool:
        return self.low <= other.low < other.too_high <= self.too_high

    def clamp(self, val: int) -> int:
        return min(max(val, self.low), self.too_high - 1)

    def wrap(self, val: int) -> int:
        if val in self:
            return val
        x = (val - self.low) % len(self)
        return self.low + x


@dataclass(slots=True)
class BoundingBox2D:
    x_axis: Range = field(default_factory=Range)
    y_axis: Range = field(default_factory=Range)

    def clear(self) -> None:
        self.x_axis.clear()
        self.y_axis.clear()

    def expand_to(self, p: Point2D) -> None:
        self.x_axis.expand_to(p.x)
        self.y_axis.expand_to(p.y)

    def contract_by(self, amount: int) -> None:
        self.x_axis.low += amount
        self.x_axis.too_high -= amount
        self.y_axis.low += amount
        self.y_axis.too_high -= amount

    def wrap(self, p: Point2D) -> Point2D:
        return Point2D(self.x_axis.wrap(p.x), self.y_axis.wrap(p.y))

    def __contains__(self, p: Point2D) -> bool:
        return p.x in self.x_axis and p.y in self.y_axis

    def __iter__(self) -> Iterator[Point2D]:
        for y in self.y_axis:
            for x in self.x_axis:
                yield Point2D(x, y)


@dataclass(slots=True)
class BoundingBox3D:
    x_axis: Range = field(default_factory=Range)
    y_axis: Range = field(default_factory=Range)
    z_axis: Range = field(default_factory=Range)

    def clear(self) -> None:
        self.x_axis.clear()
        self.y_axis.clear()
        self.z_axis.clear()

    def expand_to(self, p: Point3D) -> None:
        self.x_axis.expand_to(p.x)
        self.y_axis.expand_to(p.y)
        self.z_axis.expand_to(p.z)

    def __contains__(self, p: Point3D) -> bool:
        return p.x in self.x_axis and p.y in self.y_axis and p.z in self.z_axis
