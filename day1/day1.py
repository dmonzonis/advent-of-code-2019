def total_required_fuel(mass_list):
    return sum(required_fuel(mass) for mass in mass_list)


def required_fuel(mass):
    return mass // 3 - 2


def main():
    with open("input.txt") as f:
        lines = [int(x) for x in f.read().splitlines()]
    print(total_required_fuel(lines))


if __name__ == "__main__":
    main()