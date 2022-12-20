class StrComparer:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def __lt__(self, other) -> bool:
        return self.value + other.value < other.value + self.value

    def __gt__(self, other) -> bool:
        return self.value + other.value > other.value + self.value


def largest_number(n: int, numbers: str) -> str:
    splitted_numbers: list[str] = numbers.split(' ')
    splitted_numbers.sort(key=StrComparer, reverse=True)
    result: str = ''.join(splitted_numbers).lstrip('0')
    return (result if result != '' else '0')


def main() -> None:
    n: int = int(input())
    numbers: str = input()
    print(largest_number(n, numbers))


if __name__ == '__main__':
    main()
