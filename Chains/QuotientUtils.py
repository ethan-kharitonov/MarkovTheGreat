
from functools import cache
from typing import List
from bisect import bisect_left
from State import State

# ========= Constants ========= #
HEALTH_MAP = {0: 'S', 1: 'I', 2: 'R'}
INV_HEALTH_MAP = {'S': 0, 'I': 1, 'R': 2}


def decode_index(index: int, base: int, length: int) -> List[int]:
    digits = [0] * length
    for i in range(length - 1, -1, -1):
        digits[i] = index % base
        index //= base
    return digits


def encode_state(state: State, H: int) -> int:
    N = len(state.health_vector)
    base = 3 * H
    index = 0
    for i in range(N):
        h = INV_HEALTH_MAP[state.health_vector[i]]
        l = state.location_vector[i]
        digit = h * H + l
        index = index * base + digit
    return index


def decode_state(index: int, N: int, H: int) -> State:
    base = 3 * H
    digits = decode_index(index, base, N)
    health_vector = []
    location_vector = []
    for d in digits:
        h, l = divmod(d, H)
        health_vector.append(HEALTH_MAP[h])
        location_vector.append(l)
    return State(health_vector=health_vector, location_vector=location_vector)


def count_disease_free_below(index: int, N: int, H: int) -> int:
    base = 3 * H
    digits = decode_index(index, base, N)

    @cache
    def count_prefix(pos: int, tight: bool) -> int:
        if pos == N:
            return 1

        max_digit = digits[pos] if tight else base - 1
        total = 0
        for d in range(max_digit + 1):
            h, _ = divmod(d, H)
            if h == 1:
                continue
            next_tight = tight and (d == max_digit)
            total += count_prefix(pos + 1, next_tight)
        return total

    return count_prefix(0, True)


class TransientRank:
    def __init__(self, N: int, H: int):
        self.N = N
        self.H = H
        self.size = (3 * H) ** N

    def __getitem__(self, j: int) -> int:
        return j - count_disease_free_below(j, self.N, self.H)

    def __len__(self) -> int:
        return self.size


def get_transient_state(i: int, N: int, H: int) -> State:
    j = bisect_left(TransientRank(N, H), i)
    return decode_state(j, N, H)
