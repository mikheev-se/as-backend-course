def psp(n: int, counter_open: int = 0, counter_close: int = 0, ans: str = '') -> None:
    if counter_open + counter_close == 2 * n:
        print(ans)
        return
    if counter_open < n:
        psp(n, counter_open + 1, counter_close, ans + '(')
    if counter_open > counter_close:
        psp(n, counter_open, counter_close + 1, ans + ')')


def main() -> None:
    psp(int(input()))


if __name__ == '__main__':
    main()
