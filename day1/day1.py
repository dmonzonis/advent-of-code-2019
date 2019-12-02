def required_fuel(mass):
    return mass // 3 - 2


def required_fuel_recursive(mass):
    total = 0
    fuel = required_fuel(mass)
    while fuel >= 0:
        total += fuel
        fuel = required_fuel(fuel)
    return total


def total_required_fuel(mass_list, recursive=False):
    if recursive:
        fuel_func = required_fuel_recursive
    else:
        fuel_func = required_fuel
    return sum(fuel_func(mass) for mass in mass_list)


def main():
    with open("input.txt") as f:
        lines = [int(x) for x in f.read().splitlines()]

    # Part 1
    print(total_required_fuel(lines))

    # Part 2
    print(total_required_fuel(lines, True))


if __name__ == "__main__":
    main()

