def isPalindrome(s: str) -> bool:
    string = s.lower()
    to_compare = ''
    for letter in string:
        if letter.isalpha() or letter.isnumeric():
            to_compare = to_compare + letter

    return to_compare == to_compare[::-1]


def main():
    print(isPalindrome(input()))


if __name__ == '__main__':
    main()
