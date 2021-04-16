class BST:
    def __init__(self, elements=None) -> None:
        elements = elements if elements is not None else list()
        self.root = None
        self.max_word_len = 0
        for element in elements:
            self.insert(element)

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.root.insert(value)

    def search(self, value):
        return self.root.search(value)

    def remove(self, value):
        result = self.search(value)
        if result is not None:
            result.remove(tree)

    def min(self):
        return self.root.min()

    def max(self):
        return self.root.max()

    def print(self):
        if self.root is None:
            print("Drzwo jest puste - nie można wydrukować")
            return

        def max_word_len():
            return self.root.get_max_word_len(0)
        max_depth = self.get_max_depth()
        max_word = max_word_len()
        values = dict()
        for i in range(max_depth):
            values[i] = [" "*(max_word) for _ in range(2**i)]
        self.root.add_node_to_list(values, 0, 0)
        length = (max_word + 1) * 2 ** max_depth
        i = 0
        for key in range(max_depth):
            for numb in values[key]:
                print(str(numb).center(length//2**i), end="")
            print()
            i += 1

    def get_max_depth(self):
        self.root.update_depth(start_depth=1)
        return self.root.get_max_depth()


class Node:
    def __init__(self, value, parent=None, left=None, right=None) -> None:
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    def insert(self, value):
        if value > self.value:
            if self.right is None:
                self.right = Node(value=value, parent=self)
            else:
                self.right.insert(value)
        else:
            if self.left is None:
                self.left = Node(value, parent=self)
            else:
                self.left.insert(value)

    def max(self):
        if self.right is None:
            return self
        return self.right.max()

    def min(self):
        if self.left is None:
            return self
        return self.left.min()

    def search(self, value):
        if self.value == value:
            return self
        elif value > self.value:
            if self.right is None:
                return None
            else:
                return self.right.search(value)
        else:
            if self.left is None:
                return None
            else:
                return self.left.search(value)

    def remove(self, tree):
        if self.right is None and self.left is None:
            if self.parent is None:
                tree.root = None
            else:
                if self is self.parent.right:
                    self.parent.right = None
                else:
                    self.parent.left = None
        elif self.right is None:
            if self.parent is None:
                self.left.parent = None
                tree.root = self.left
            else:
                if self is self.parent.right:
                    self.parent.right = self.left
                else:
                    self.parent.left = self.left
        elif self.left is None:
            if self.parent is None:
                self.right.parent = None
                tree.root = self.right
            else:
                if self is self.parent.right:
                    self.parent.right = self.right
                else:
                    self.parent.left = self.right
        else:
            if self.parent is None:
                self.left.parent = None
                self.right.parent = self.left
                tree.root = self.left
            else:
                result = self.left.max()
                self.value = result.value
                result.remove(tree=tree)

    def update_depth(self, start_depth):
        self.depth = start_depth
        if self.right is not None:
            self.right.update_depth(self.depth+1)
        if self.left is not None:
            self.left.update_depth(self.depth+1)

    def __str__(self):
        return f'Moja wartosc: {self.value}, glebokosc: {self.depth}'

    def get_max_depth(self):
        if self.left is None and self.right is None:
            return self.depth
        elif self.left is None:
            return self.right.get_max_depth()
        elif self.right is None:
            return self.left.get_max_depth()
        return max(self.left.get_max_depth(), self.right.get_max_depth())

    def get_max_word_len(self, max_len):
        if self.left is None and self.right is None:
            return max(len(str(self.value)), max_len)
        elif self.left is None:
            return self.right.get_max_word_len(max(max_len, len(str(self.value))))
        elif self.right is None:
            return self.left.get_max_word_len(max(max_len, len(str(self.value))))
        return max(self.left.get_max_word_len(max(max_len, len(str(self.value)))), self.right.get_max_word_len(max(max_len, len(str(self.value)))))

    def add_node_to_list(self, values, x, y):
        values[y][x] = self.value
        if self.left is not None and self.right is not None:
            self.right.add_node_to_list(values, 2*x+1, y+1)
            self.left.add_node_to_list(values, 2*x, y+1)
        elif self.left is None and self.right is not None:
            self.right.add_node_to_list(values, 2*x+1, y+1)
        elif self.right is None and self.left is not None:
            self.left.add_node_to_list(values, 2*x, y+1)


tree = BST()
while True:
    inputed = input("Opcja: ")
    if inputed in {'1'}:
        tree.insert(int(input("Jaką wartość dodać do drzewa: ")))
    elif inputed in {'2'}:
        tree.remove(int(input("Jaką wartość usunac z drzewa: ")))
    elif inputed in {'3'}:
        print(tree.max().value)
    elif inputed in {'4'}:
        print(tree.min().value)
    elif inputed in {'5'}:
        tree.print()
