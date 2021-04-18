from matplotlib import pyplot as plt
from timeit import timeit
import random


def generate_values():
    numbers = [random.randint(1, 30000) for _ in range(10000)]
    return numbers


def remove_items(tree, list_of_numbers, n):
    for number in list_of_numbers[:n]:
        tree.remove(number)


def search_items(tree, list_of_numbers, n):
    for number in list_of_numbers[:n]:
        tree.search(number)


def add_items(tree, list_of_numbers, n):
    for number in list_of_numbers[:n]:
        tree.insert(number)


def generate_plot(xvalues, yvaluesbst, yvaluesavl, title, filename):
    plt.plot(xvalues, yvaluesbst, label="BST")
    plt.plot(xvalues, yvaluesavl, label="AVL")
    plt.title(title)
    plt.legend()
    plt.yscale("log")
    plt.savefig(filename)
    plt.clf()


if __name__ == "__main__":
    list_of_numbers = generate_values()
    arguments = [1000, 2000, 5000, 10000]
    bst_insert_times = []
    bst_search_times = []
    bst_remove_times = []
    avl_insert_times = []
    avl_search_times = []
    avl_remove_times = [0, 0, 0, 0]
    # avl_remove_times = []
    for arg in arguments:
        bst_insert_times.append(timeit(f'add_items(tree, {list_of_numbers}, {arg})', setup="from main import BST; from generate_plots import add_items; tree=BST()", number=1))
        avl_insert_times.append(timeit(f'add_items(tree, {list_of_numbers}, {arg})', setup="from main import AVL; from generate_plots import add_items; tree=AVL()", number=1))

        bst_search_times.append(timeit(f'search_items(tree, {list_of_numbers}, {arg})', setup=f"from main import BST; from generate_plots import search_items; tree=BST({list_of_numbers[:arg]})", number=1))
        avl_search_times.append(timeit(f'search_items(tree, {list_of_numbers}, {arg})', setup=f"from main import AVL; from generate_plots import search_items; tree=AVL({list_of_numbers[:arg]})", number=1))

        bst_remove_times.append(timeit(f'remove_items(tree, {list_of_numbers}, {arg})', setup=f"from main import BST; from generate_plots import remove_items; tree=BST({list_of_numbers[:arg]})", number=1))
        # Niestety nie działa :(
        # avl_remove_times.append(timeit(f'remove_items(tree, {list_of_numbers}, {arg})', setup=f"from main import AVL; from generate_plots import remove_items; tree=AVL({list_of_numbers[:arg]})", number=1))
    print(bst_insert_times)
    print(avl_insert_times)

    print(bst_search_times)
    print(avl_search_times)

    print(bst_remove_times)
    print(avl_remove_times)

    generate_plot(arguments, bst_insert_times, avl_insert_times, "Time for insert elements", "insert_times.png")
    generate_plot(arguments, bst_search_times, avl_search_times, "Time for search elements", "search_times.png")
    generate_plot(arguments, bst_remove_times, avl_remove_times, "Time for remove elements", "remove_times.png")
