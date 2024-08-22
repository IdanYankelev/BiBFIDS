import mmh3
from bitarray import bitarray

size = None

def set_bf_size(bf_size):
    global size
    size = bf_size


class BloomFilter:
    def __init__(self, hash_count=100):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.number_insertions = 0

    def add(self, item):
        # if not self.check(item):
        self.number_insertions += 1
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            self.bit_array[digest] = 1

    def check(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == 0:
                return False
        return True

    def clear(self):
        self.bit_array.setall(0)
