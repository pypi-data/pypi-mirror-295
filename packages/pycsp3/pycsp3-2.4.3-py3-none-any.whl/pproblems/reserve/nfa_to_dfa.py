nfa = {'A': {'a': ['A', 'B'], 'b': ['A']}, 'B': {'a': ['C'], 'b': ['C']}, 'C': {'a': ['D'], 'b': ['D']}, 'D': {'a': [], 'b': []}}
start = 'A'
finals = ['D']
symbols = list(nfa[start].keys())
print(nfa)

transitions = [(state1, symbol, state2) for state1 in nfa.keys() for symbol in symbols for state2 in nfa[state1][symbol]]
nfa = {}
for state1, symbol, state2 in transitions:
    if state1 not in nfa:
        nfa[state1] = {}
    if symbol not in nfa[state1]:
        nfa[state1][symbol] = []
    nfa[state1][symbol].append(state2)
print(nfa)

states = []
dfa = {}

queue = [start]
while len(queue) != 0:
    state1 = queue.pop(0)
    dfa[state1] = {}
    tokens = [v for v in state1.split('_')]
    for symbol in symbols:
        state2 = "_".join(v for tok in tokens if tok in nfa for v in nfa[tok][symbol])
        dfa[state1][symbol] = state2
        if state2 not in states:
            queue.append(state2)
            states.append(state2)

print(dfa)

dfa_final = [state for state in list(dfa.keys()) if any(tok in finals for tok in state.split('_'))]
print(dfa_final)
