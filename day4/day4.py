def find_valid_passwords_in_range(min_val, max_val, part2=False):
    valid = []
    for password in range(min_val, max_val + 1):
        if is_valid_password(password, part2):
            valid.append(password)
    return valid


def is_valid_password(password, part2=False):
    digits = [int(x) for x in str(password)]
    has_dubs = False
    i = 0
    while i < len(digits) - 1:
        if digits[i] > digits[i + 1]:
            return False  # Digits cannot be decreasing
        repeats = 0
        while i < len(digits) - 1 and digits[i] == digits[i + 1]:
            repeats += 1
            i += 1
        if (part2 and repeats == 1) or (not part2 and repeats != 0):
            has_dubs = True
        if repeats == 0:
            i += 1
    return has_dubs


def main():
    # Part 1
    valid_passwords = find_valid_passwords_in_range(264793, 803935)
    print(len(valid_passwords))

    # Part 2
    valid_passwords = find_valid_passwords_in_range(264793, 803935, True)
    print(len(valid_passwords))


if __name__ == "__main__":
    main()
