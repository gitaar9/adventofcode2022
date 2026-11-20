
class Animal(object):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return self.name


def add(left: int, right: int) -> int:
    return left + right


print(add(9, 10))

a = Animal('dog')
print(type(a))
a.name = 'something else'
print(a)
