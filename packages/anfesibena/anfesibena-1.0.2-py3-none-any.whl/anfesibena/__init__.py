class Anfesibena:
    def __div__(self, other):
        return self * (other**-1)

    def __neg__(self):
        return self * -1

    def __rdiv__(self, other):
        return other * (self**-1)

    def __rsub__(self, other):
        return other + (self * -1)

    def __rtruediv__(self, other):
        return other * (self**-1)

    def __sub__(self, other):
        return self + (other * -1)

    def __truediv__(self, other):
        return self * (other**-1)
