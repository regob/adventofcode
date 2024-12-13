from dataclasses import dataclass

@dataclass(slots=True)
class v2:
    x: float
    y: float

    def __add__(self, v):
        return v2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return v2(self.x - v.x, self.y - v.y)

    def __mul__(self, c):
        if isinstance(c, v2):
            return self.x * c.x + self.y * c.y
        if isinstance(c, float | int):
            return v2(self.x * c, self.y * c)
        raise ValueError('v2 can only be multiplied by a number or a v2.')

    def __rmul__(self, other):
        return self * other     # multiplication is commutative (no dyadic product implemented)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, v2) and (self.x, self.y) == (value.x, value.y)

    def __iter__(self):
        yield from (self.x, self.y)
        
