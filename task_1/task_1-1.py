def nearest_zero(lands):
    empty_land_mark = 0
    result = []

    for i in range(len(lands)):
        try:
            left_range = lands[:i][::-1].index(empty_land_mark) + 1
        except ValueError:
            left_range = float('inf')

        try:
            right_range = lands.index(empty_land_mark, i, len(lands)) - i
        except ValueError:
            right_range = float('inf')

        result.append(min(left_range, right_range))

    return result


if __name__ == '__main__':
    lands = list(map(int, input().split(' ')))
    result = nearest_zero(lands=lands)
    print(' '.join(str(item) for item in result))
