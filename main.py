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
            inserted = self.root.insert(value)
            return inserted

    def search(self, value):
        return self.root.search(value)

    def remove(self, value):
        result = self.search(value)
        if result is not None:
            result.remove(self)

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


class AVL(BST):
    def __init__(self, elements=None) -> None:
        elements = elements if elements is not None else list()
        self.root = None
        self.max_word_len = 0
        for element in elements:
            self.insert(element)

    def insert(self, value):
        inserted = super().insert(value)
        if inserted is not None:
            inserted.change_balance(self)

    def remove(self, value):
        result = self.search(value)
        if result is not None:
            deleted, left_son = result.remove(self)
            if deleted is not None:
                deleted.change_balance_remove(self, left_son)


class Node:
    def __init__(self, value, parent=None, left=None, right=None, balance=0) -> None:
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.balance = balance

    def rotate(self, direction, tree):
        if direction == "left":
            self.right.parent = self.parent
            if self.parent is not None:
                if self.parent.right is self:
                    self.parent.right = self.right
                else:
                    self.parent.left = self.right
            else:
                tree.root = self.right
            self.parent = self.right
            if self.right.left is not None:
                self.right.left.parent, self.right.left, self.right = self, self, self.right.left
            else:
                self.right.left, self.right = self, self.right.left
        else:
            self.left.parent = self.parent
            if self.parent is not None:
                if self.parent.right is self:
                    self.parent.right = self.left
                else:
                    self.parent.left = self.left
            else:
                tree.root = self.left
            self.parent = self.left
            if self.left.right is not None:
                self.left.right.parent, self.left.right, self.left = self, self, self.left.right
            else:
                self.left.right, self.left = self, self.left.right

    def fix_tree(self, tree):
        if self.balance == -2:
            if self.left.balance == -1 or self.balance == 0:
                if self.left.balance == -1:
                    self.balance = 0
                    self.left.balance = 0
                else:
                    self.left.balance = 0
                    self.balance = 1
                self.rotate("right", tree)
            else:
                if self.left.right.balance == -1:
                    self.balance = 0
                    self.left.balance = -1
                elif self.left.right.balance == 0:
                    self.balance = 0
                    self.left.balance = 0
                else:
                    self.balance = -1
                    self.left.balance = 0
                self.left.right.balance = 0
                self.left.rotate("left", tree)
                self.rotate("right", tree)
        elif self.balance == 2:
            if self.right.balance == 1 or self.right.balance == 0:
                if self.right.balance == 1:
                    self.balance = 0
                    self.right.balance = 0
                else:
                    self.right.balance = 0
                    self.balance = -1
                self.balance = 0
                self.right.balance = 0
                self.rotate("left", tree)
            else:
                if self.right.left.balance == -1:
                    self.balance = 0
                    self.right.balance = 1
                elif self.right.left.balance == 0:
                    self.balance = 0
                    self.right.balance = 0
                else:
                    self.balance = 1
                    self.right.balance = 0
                self.right.left.balance = 0
                self.right.rotate("right", tree)
                self.rotate("left", tree)

    def change_balance(self, tree):
        if self.balance > 1 or self.balance < -1:
            self.fix_tree(tree)
            return
        if self.parent is None:
            return None
        if self.parent.left is self:
            self.parent.balance -= 1
        else:
            self.parent.balance += 1
        if self.parent.balance != 0:
            self.parent.change_balance(tree)

    def change_balance_remove(self, tree, left_son):
        if self.balance > 1 or self.balance < -1:
            self.fix_tree(tree)
            self.parent.change_balance_remove(tree, left_son)
        if self.parent is None:
            return None
        if left_son:
            self.parent.balance += 1
        else:
            self.parent.balance -= 1
        if self.parent.balance != 0:
            self.parent.change_balance_remove(tree, left_son)

    def insert(self, value):
        if value > self.value:
            if self.right is None:
                self.right = Node(value=value, parent=self)
                return self.right
            else:
                return self.right.insert(value)
        else:
            if self.left is None:
                self.left = Node(value, parent=self)
                return self.left
            else:
                return self.left.insert(value)

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
                return None, None
            else:
                if self is self.parent.right:
                    self.parent.right = None
                    return self, False
                else:
                    self.parent.left = None
                    return self, True
        elif self.right is None:
            if self.parent is None:
                self.left.parent = None
                tree.root = self.left
                return None, None
            else:
                if self is self.parent.right:
                    self.parent.right = self.left
                    return self, False
                else:
                    self.parent.left = self.left
                    return self, True
        elif self.left is None:
            if self.parent is None:
                self.right.parent = None
                tree.root = self.right
                return None, None
            else:
                if self is self.parent.right:
                    self.parent.right = self.right
                    return self, False
                else:
                    self.parent.left = self.right
                    return self, True
        else:
            if self.parent is None:
                self.left.parent = None
                self.left.right = self.right
                self.right.parent = self.left
                tree.root = self.left
                return None, None
            else:
                result = self.left.max()
                self.value = result.value
                return result.remove(tree=tree)

    def update_depth(self, start_depth):
        self.depth = start_depth
        if self.right is not None:
            self.right.update_depth(self.depth+1)
        if self.left is not None:
            self.left.update_depth(self.depth+1)

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


tree = AVL([5, 3, 4, 7, 9, 1, 8, 6])
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
