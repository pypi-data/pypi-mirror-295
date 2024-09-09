class Scaevola:
    def __ge__(self, other):
        return type(self)(other) <= self

    def __gt__(self, other):
        return type(self)(other) < self

    def __radd__(self, other):
        return type(self)(other) + self

    def __rand__(self, other):
        return type(self)(other) & self

    def __rdivmod__(self, other):
        return divmod(type(self)(other), self)

    def __rfloordiv__(self, other):
        return type(self)(other) // self

    def __rlshift__(self, other):
        return type(self)(other) << self

    def __rmatmul__(self, other):
        return type(self)(other) @ self

    def __rmod__(self, other):
        return type(self)(other) % self

    def __rmul__(self, other):
        return type(self)(other) * self

    def __ror__(self, other):
        return type(self)(other) | self

    def __rpow__(self, other):
        return type(self)(other) ** self

    def __rrshift__(self, other):
        return type(self)(other) >> self

    def __rsub__(self, other):
        return type(self)(other) - self

    def __rtruediv__(self, other):
        return type(self)(other) / self

    def __rxor__(self, other):
        return type(self)(other) ^ self
