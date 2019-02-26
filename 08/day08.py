class Node:
    def __init__(self):
        self.children = []
        self.metadata = []

    def add_child(self, child):
        self.children.append(child)

    def add_metadata(self, data):
        self.metadata.append(data)

    def __str__(self):
        return self.str_helper(0)

    def str_helper(self, depth):
        """Used for a nicer input using print"""
        result = ""
        for i in range(depth):
            result += "\t"
        result += "A node with metadata ("
        result += ','.join(map(str, self.metadata))
        result += ") and "
        result += str(len(self.children))
        result += " children: \n"
        for child in self.children:
            result += child.str_helper(depth+1)
        return result

    def metadata_sum(self):
        result = 0
        for data in self.metadata:
            result += data
        for child in self.children:
            result += child.metadata_sum()
        return result

    def node_value(self):
        result = 0
        if len(self.children) == 0:
            for data in self.metadata:
                result += data
            return result

        for data in self.metadata:
            if data in range(1, len(self.children)+1):
                result += self.children[data-1].node_value()
        return result


def read_node(nums):
    """Returns a pair: first part is a new node, second part is remaining numbers"""
    children_num = nums[0]
    metadata_num = nums[1]
    result = Node()
    remaining = nums[2:]
    for i in range(children_num):
        child, remaining = read_node(remaining)
        result.add_child(child)
    for i in range(metadata_num):
        result.add_metadata(remaining[0])
        remaining = remaining[1:]
    return result, remaining


def load_input():
    with open("input.txt", "r") as puzzle_input:
        line = puzzle_input.read()
    return [int(s) for s in line.split()]


def main():
    numbers = load_input()
    tree, remaining = read_node(numbers)

    if len(remaining) != 0:
        raise ValueError("Did not read whole input.")

    print(tree.metadata_sum())  # part 1
    print(tree.node_value())  # part 2


main()
