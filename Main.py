from Chains.QuotientUtils import decode_state, get_transient_state
from State import State


N = H = 3
num_states = (3 * H) ** N
num_absorbing_states = (2 * H) ** N

def rank(state: State) -> int:
    INV_HEALTH_MAP = {'S': 0, 'I': 1, 'R': 2}
    answer = 0
    for i in range(N):
        answer += INV_HEALTH_MAP[state.health_vector[i]]

    return answer

for i in range(num_absorbing_states):
    state = get_transient_state(i, N, H)
    print(f'{get_transient_state(i, N, H)}, rank = {rank(state)}')