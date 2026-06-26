from collections import Counter


def top(counter: Counter, n: int = 10):
    return counter.most_common(n)