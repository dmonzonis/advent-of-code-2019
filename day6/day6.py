def generate_tree(orbits):
    # the tree dict maps a node to its parent
    tree = {}
    for orbit in orbits:
        parent, child = orbit.split(')')
        tree[child] = parent
    return tree


def count_edges_to_root(tree, node):
    count = 0
    while node in tree:
        count += 1
        node = tree[node]
    return count


def count_edges_to_parent(tree, node, parent):
    count = 0
    while node in tree and node != parent:
        count += 1
        node = tree[node]
    if node != parent:
        # Was not a parent node
        return float('inf')
    return count


def count_total_orbits(tree):
    count = 0
    for node in tree:
        count += count_edges_to_root(tree, node)
    return count


def find_first_common_node(tree, node1, node2):
    # Get all nodes up to the root from node1 in a set
    path1 = set()
    while node1 in tree:
        path1.add(node1)
        node1 = tree[node1]
    # Now traverse back from node2 until we find a common node
    while node2 in tree:
        if node2 in path1:
            return node2
        node2 = tree[node2]
    return None


def calculate_orbital_transfers(tree, node1, node2):
    count = 0
    common = find_first_common_node(tree, node1, node2)
    # Count steps to reach the common node for each of the nodes
    count += count_edges_to_parent(tree, node1, common)
    count += count_edges_to_parent(tree, node2, common)
    return count - 2  # Remove 2 from the nodes themselves


def main():
    with open("input.txt") as f:
        orbits = f.read().splitlines()

    # Part 1
    tree = generate_tree(orbits)
    print(count_total_orbits(tree))

    # Part 2
    print(calculate_orbital_transfers(tree, 'YOU', 'SAN'))


if __name__ == "__main__":
    main()
