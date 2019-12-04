def find_valid_passwords_in_range(min_val, max_val):
    valid = []
    for password in range(min_val, max_val + 1):
        if is_valid_password(password):
            valid.append(password)
    return valid


def is_valid_password(password):
    digits = [int(x) for x in str(password)]
    has_dubs = False
    for i in range(len(digits) - 1):
        if digits[i] > digits[i + 1]:
            return False  # Digits cannot be decreasing
        if digits[i] == digits[i + 1]:
            has_dubs = True
    return has_dubs


def main():
    # Part 1
    valid_passwords = find_valid_passwords_in_range(264793, 803935)
    print(len(valid_passwords))


if __name__ == "__main__":
    main()
