import sys


class hashtable:
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity
        self.load_factor = 0.7

    def __hash(self, key):
        return key % self.capacity

    def insert(self, key, value):
        index = self.__hash(key)
        # check load factor
        if (self.size) / self.capacity > self.load_factor:
            return 0
        if self.table[index] is None:
            self.table[index] = self.Node(key, value)
        else:
            # Collision resolution using chaining
            current = self.table[index]
            # Check if key already exists
            while current is not None:
                if current.key == key:
                    # Update value if key exists
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            # Add new node at the end of the chain
            current.next = self.Node(key, value)

    def output(self):
        for i in range(self.capacity):
            current = self.table[i]
            if current is not None:
                while current is not None:
                    print(
                        f"[{current.key}, {current.value[0]} , {current.value[2]}, {current.value[1]}, {float(current.value[3]):.2g}]",
                        end=' ')
                    current = current.next
                print()
            else:
                print()

    def search(self, search_id):
        index = self.__hash(search_id)
        current = self.table[index]
        while current:
            if current.key == search_id:
                print(f"[{current.key}, {current.value[0]} , {current.value[1]}, {current.value[2]}, {float(current.value[3]):.2g}]")
                return None
            current = current.next
        print('KHONG TIM THAY')


def main():
    x = sys.stdin.readline()
    table = hashtable(int(x))
    for _ in range(int(x)):
        k = sys.stdin.readline()
        table.size += int(k)
        for _ in range(int(k)):
            id = sys.stdin.readline()
            name = sys.stdin.readline().strip()
            year = sys.stdin.readline().strip()
            gender = sys.stdin.readline().strip()
            grade = sys.stdin.readline().strip()
            table.insert(int(id), [name, year, gender, grade])
    search_attempts = sys.stdin.readline()
    for _ in range(int(search_attempts)):
        search_id = sys.stdin.readline()
        table.search(int(search_id))
if __name__ == "__main__":
    main()