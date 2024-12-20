from collections import defaultdict

class State:

    def __init__(self, name, transitions=None):
        self.name = name
        self.transitions = transitions or defaultdict(list)
        self.counter = 0

    def add_transition(self, symbol, state):
        self.transitions[symbol].append(state)

    def __repr__(self):
        return f"State {self.state_id}: ({self.name})"

    def __str__(self):
        return self.name

class NFA:
    def __init__(self):
        self.start_state = State("Start")

    def reset_counter(self):
        current_states = [self.start_state]
        while len(current_states) > 0:
            next_states = []
            for state in current_states:
                state.counter = 0
                for successors in state.transitions.values():
                    for next_state in successors:
                        if next_state != self.start_state:
                            next_states.append(next_state)
            current_states = next_states

    def accepts(self, string):
        self.reset_counter()
        current_states = self.start_state.transitions[None]
        for symbol in string:
            next_states = []
            for state in set(current_states):
                state.counter += 1
                succ = state.transitions[symbol]
                trans_succ = self.transitive_closure(succ)
                next_states.extend(trans_succ)
            current_states = next_states
        accepted_counter = 0
        for state in current_states:
            state.counter += 1
            if state == self.start_state:
                accepted_counter += state.counter
        print(f"Word: {string}, Start Counter: {accepted_counter}")
        return self.start_state in current_states

    def transitive_closure(self, states):
        trans_succ = set(states)
        while True:
            length = len(trans_succ)
            for s in states:
                lst = s.transitions[None]
                trans_succ.update(lst)
            if len(trans_succ) == length: break
        return trans_succ

    def add_pattern(self, pattern):
        next_state = self.start_state
        state = self.start_state
        for i in range(len(pattern)-1, -1, -1):
            symbol = pattern[i]
            state = State(pattern[:i]+"["+symbol+"]" +pattern[i+1:])
            state.add_transition(symbol, next_state)
            next_state = state
        self.start_state.add_transition(None, state)

if __name__ == "__main__":
    nfa = NFA()
    nfa.add_pattern("abc")
    assert nfa.accepts("abc")
    assert not nfa.accepts("ab")
    assert not nfa.accepts("abcd")
    assert nfa.accepts("abcabc")