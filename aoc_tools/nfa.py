from collections import defaultdict

class State:

    def __init__(self, name, transitions=None):
        self.name = name
        self.transitions = transitions or defaultdict(list)

    def add_transition(self, symbol, state):
        self.transitions[symbol].append(state)

    def __repr__(self):
        return f"State {self.name}"

    def __str__(self):
        return self.name

class NFA:
    def __init__(self):
        self.start_state = State("Start")

    def accepts(self, string):
        current_states = [(1, state) for state in self.start_state.transitions[None]]
        for symbol in string:
            next_states = []
            #how many start states do we pass this round?
            start_state_count = sum([count for count, state in current_states if state == self.start_state])
            while current_states:
                count, state = current_states.pop()
                # all new patterns start with the start state count, but only once
                if state == self.start_state and start_state_count > 0:
                    current_states.extend([(start_state_count, state) for state in self.start_state.transitions[None]])
                    start_state_count = 0
                else:
                    transitions = state.transitions[symbol]
                    next_states.extend([(count, state) for state in transitions])
            current_states = next_states
        result = sum([count for count, state in current_states if state == self.start_state])
        return result

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
    nfa.add_pattern("a")
    nfa.add_pattern("ab")
    nfa.add_pattern("c")
    nfa.add_pattern("bc")
    nfa.add_pattern("d")

    assert nfa.accepts("ab") == 1
    assert nfa.accepts("abc") == 2
    assert nfa.accepts("abcd") == 2
    assert nfa.accepts("bcd") == 1