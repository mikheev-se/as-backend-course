def parse_field(field):
    num_to_count = {}
    tokens = list(c for c in field if c.isdigit())
    for t in set(tokens):
        num_to_count[t] = tokens.count(t)

    return num_to_count


def trainer(k, field):
    score = 0
    threshold = k * 2
    num_to_count = parse_field(field=field)

    for k, v in num_to_count.items():
        if v < threshold:
            score = score + 1

    return score


if __name__ == '__main__':
    k = int(input())
    field = ''
    for _ in range(4):
        field = field + input()
    score = trainer(k, field)

    print(score)
