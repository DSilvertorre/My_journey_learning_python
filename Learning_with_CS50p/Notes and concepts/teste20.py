class Jar:
    def __init__(self, capacity=12):
        self._capacity = capacity
        self._size = 0
        if capacity < 0:
            raise ValueError


    def __str__(self):
        return "🍪" * self.size

    def deposit(self, n):
        if n + self.size > self.capacity:
            raise ValueError
        else: self._size += n

    def withdraw(self, n):
        if n > self.size:
            raise ValueError
        else: self._size -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size