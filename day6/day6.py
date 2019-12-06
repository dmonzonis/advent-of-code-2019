def generate_tree(orbits):
    # the tree dict maps a node to its parent
    tree = {}
    for orbit in orbits:
        parent, child = orbit.split(')')
        tree[child] = parent
    return tree


def count_edges_to_parent(tree, node):
    count = 0
    while node in tree:
        count += 1
        node = tree[node]
    return count


def count_total_orbits(tree):
    count = 0
    for node in tree:
        count += count_edges_to_parent(tree, node)
    return count


def main():
    with open("input.txt") as f:
        orbits = f.read().splitlines()
    
    # Part 1
    tree = generate_tree(orbits)
    print(count_total_orbits(tree))


if __name__ == "__main__":
    main()
