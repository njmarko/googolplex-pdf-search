"""
Author: Marko Njegomir sw-38-2018
"""



class Heap_node(object):

    def __init__(self, key, value):
        self._key = key
        self._value = value

    def get_key(self):
        return self._key

    def set_key(self, key):
        self._key = key

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def __eq__(self, other):
        return self._key == other.get_key()

    def __ne__(self, other):
        return self._key != other.get_key()

    def __lt__(self, other):
        return self._key < other.get_key()

    def __le__(self, other):
        return self._key <= other.get_key()

    def __gt__(self, other):
        return self._key > other.get_key()

    def __ge__(self, other):
        return self._key >= other.get_key()

    def __str__(self):
        return str(self._key)


class MinHeap(object):

    def __init__(self):
        self._data = []
        self._heap_size = 0

    def is_empty(self):
        return self._heap_size == 0

    def min(self):
        if self.is_empty():
            raise Exception
        return self._data[0].get_key(), self._data[0].get_value()

    def left(self, position):
        return position * 2 + 1

    def right(self, position):
        return position * 2 + 2

    def parent(self, position):
        return (position - 1) // 2

    def swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def add(self, key, value=None):

        node = Heap_node(key, value)
        self._data.append(node)
        self._heap_size += 1
        self.upheap(self._heap_size - 1)

    def upheap(self, index):
        p_index = self.parent(index)
        if p_index < 0 or self._data[index] > self._data[p_index]:
            return
        self.swap(index, p_index)
        self.upheap(p_index)

    def min(self):
        if self.is_empty():
            raise Exception
        return self._data[0].get_key(), self._data[0].get_value()

    def remove_min(self):
        if self.is_empty():
            raise Exception
        self.swap(0, self._heap_size - 1)
        ret_val = self._data.pop(self._heap_size - 1)
        ret_val = ret_val.get_key(), ret_val.get_value()
        self._heap_size -= 1
        self.downheap(0)
        return ret_val

    def has_left(self, index):
        l = self.left(index)
        return l < self._heap_size - 1

    def has_right(self, index):
        r = self.right(index)
        return r < self._heap_size - 1

    def downheap(self, index):
        l_index = self.left(index)
        r_index = self.right(index)

        min_index = index
        if l_index < self._heap_size and self._data[l_index] < self._data[index]:
            min_index = l_index

        if r_index < self._heap_size and self._data[r_index] < self._data[min_index]:
            min_index = r_index

        if min_index != index:
            self.swap(min_index, index)
            self.downheap(min_index)

    def __str__(self):
        ret_val = "["
        for node in self._data:
            if ret_val == "[":
                ret_val = ret_val + str(node)
                continue
            ret_val = ret_val + ", " + str(node)
        ret_val = ret_val + "]"
        return ret_val

    def return_data(self):
        return self._data


class MaxHeap(object):
    def __init__(self, data):
        self._data = data
        self._heap_size = len(data)
        self._build_max_heap()

    def has_left(self, index):
        l = self.left(index)
        return l < self._heap_size

    def has_right(self, index):
        r = self.right(index)
        return r < self._heap_size

    def left(self, position):
        return position * 2 + 1

    def right(self, position):
        return position * 2 + 2

    def parent(self, position):
        return (position - 1) // 2

    def swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    # def _build_max_heap(self):
    #     self._size = len(self._data)
    #
    #     start = (self._size - 1) // 2
    #     for i in range(start, -1, -1):
    #         self.m_heapify(i)

    def _build_max_heap(self):
        self._size = len(self._data)

        start = (self._size - 1) // 2
        for i in range(start, -1, -1):
            self.m_heapify(i)

    def _max_heapify(self, i):
        i_left = self.left(i)
        i_right = self.right(i)

        max = i
        if self.has_left(i) and self._data[i_left] > self._data[i]:
            max = i_left

        if self.has_right(i) and self._data[i_right] > self._data[max]:
            max = i_right

        if max != i:
            self.swap(max, i)
            self._max_heapify(max)

    def m_heapify(self, i):
        l_index = self.left(i)
        r_index = self.right(i)

        max = i
        if l_index < self._heap_size and self._data[l_index] < self._data[max]:
            max = l_index
        if self.has_right(i) and self._data[r_index] < self._data[max]:
            max = r_index

        if max != i:
            self.swap(max, i)
            self.m_heapify(max)

    def __str__(self):
        ret_val = "["
        for node in self._data:
            if ret_val == "[":
                ret_val = ret_val + str(node)
                continue
            ret_val = ret_val + ", " + str(node)
        ret_val = ret_val + "]"
        return ret_val

    def get_data(self):
        return self._data

    def sort(self):

        for i in range(self._size-1, 0, -1):
            self.swap(0, i)
            self._heap_size -= 1
            self.m_heapify(0)


def main():

    pass


if __name__ == '__main__':
    main()
