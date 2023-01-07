def base_two(n):
    a = '' if n >= 1 else '0'
    while n >= 1:
        a = str(n % 2) + a
        n = n // 2
    return int(a)


def main():
    result = base_two(int(input()))
    print(result)


if __name__ == '__main__':
    main()
