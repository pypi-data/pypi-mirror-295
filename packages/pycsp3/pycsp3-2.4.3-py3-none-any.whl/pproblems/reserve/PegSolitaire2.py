"""
See https://www.cs.york.ac.uk/aig/projects/implied/docs/CPAIOR03.pdf
English style (standard), 33 holes

python ppycsp3/pproblems/reserve/PegSolitaire.py -data=[3,3,0] -variant=english-hybrid -keephybrid

inversion i,j,t en t,i,j (mais la search -pra=0 -ela=4) n'est plus efficace)
MAIS ok pour :
# java ace PegSolitaire-english-hybrid-3-3-0.xml -varh=FraOnDom -jl=10000
# java ace PegSolitaire-english-hybrid-4-4-0.xml -jl=10000 -valh=AsgsE
"""

from pycsp3 import *

from PegSolitaire_Generator import generate_boards, build_transitions

assert variant() in {"english", "3x3", "4x4", "french", "test1", "test2"} and subvariant() is None or subvariant() == "hybrid"

origin_x, origin_y, nMoves = data

init_board, final_board = generate_boards(variant(), origin_x, origin_y)
n, m = len(init_board), len(init_board[0])
transitions = build_transitions(init_board)
nTransitions = len(transitions)

horizon = sum(sum(v for v in row if v) for row in init_board) - sum(sum(v for v in row if v) for row in final_board)
nMoves = horizon if nMoves <= 0 or horizon < nMoves else nMoves
assert 0 < nMoves <= horizon

pairs = [(i, j) for i in range(n) for j in range(m) if init_board[i][j] is not None]

# x[i,j,t] is the value at row i and column j at time t
x = VarArray(size=[nMoves + 1, n, m], dom=lambda t, i, j: {0, 1} if init_board[i][j] is not None else None)

# y[t] is the move (transition) performed at time t
y = VarArray(size=nMoves, dom=range(nTransitions))

satisfy(
    # setting the initial board
    x[0] == init_board,

    # setting the final board
    x[-1] == final_board
)

if not subvariant():
    def unchanged(i, j, t):
        valid = [k for k, tr in enumerate(transitions) if (i, j) in (tr[0:2], tr[2:4], tr[4:6])]
        if len(valid) == 0:
            return None
        return iff(conjunction(y[t] != k for k in valid), x[t, i, j] == x[t + 1, i, j])


    def to0(i, j, t):
        valid = [k for k, tr in enumerate(transitions) if (i, j) in (tr[0:2], tr[2:4])]
        if len(valid) == 0:
            return None
        return iff(disjunction(y[t] == k for k in valid), (x[t, i, j] == 1) & (x[t + 1, i, j] == 0))


    def to1(i, j, t):
        valid = [k for k, tr in enumerate(transitions) if (i, j) == tr[4:6]]
        if len(valid) == 0:
            return None
        return iff(disjunction(y[t] == k for k in valid), (x[t, i, j] == 0) & (x[t + 1, i, j] == 1))


    satisfy(
        [unchanged(i, j, t) for (i, j) in pairs for t in range(nMoves)],
        [to0(i, j, t) for (i, j) in pairs for t in range(nMoves)],
        [to1(i, j, t) for (i, j) in pairs for t in range(nMoves)]
    )

elif subvariant("hybrid"):
    def table():
        tbl = []
        for k, tr in enumerate(transitions):
            # firstly, x[t,i,j]
            t = [1 if tr[0:2] == (i, j) or tr[2:4] == (i, j) else 0 if tr[4:6] == (i, j) else ANY for i, j in pairs]
            # secondly, x[t+1,i,j]
            t += [0 if tr[0:2] == (i, j) or tr[2:4] == (i, j) else 1 if tr[4:6] == (i, j) else eq(col(k)) for k, (i, j) in enumerate(pairs)]
            # t += [0 if tr[0:2] == (i, j) or tr[2:4] == (i, j) else 1 if tr[4:6] == (i, j) else eq(col(i*m+j)) for l, (i, j) in enumerate(pairs)]
            # fot testing that we can detect bad indexes
            # lastly, the transition (move)
            t.append(k)
            tbl.append(tuple(t))
        return tbl


    T = table()

    satisfy(
        (x[t], x[t + 1], y[t]) in T for t in range(nMoves)
    )

    # satisfy(
    #     Sum(x[18,2:5, 3:6]) == 0
    # )

test = False
if test:
    transitions_pegs = [{i1 * m + j1, i2 * m + j2, i3 * m + j3} for i1, j1, i2, j2, i3, j3 in transitions]
    independent_transitions = [(k2, k1) for k1, k2 in combinations(nTransitions, 2) if len(transitions_pegs[k1].intersection(transitions_pegs[k2])) == 0]

    satisfy(
        (y[i], y[i + 1]) not in independent_transitions for i in range(nMoves - 1)
    )

""" Comments
1) x[0] == init_board is possible because cells with None (either in variables or values) are discarded
   This is equivalent to [x[0][i][j] == init_board[i][j] for (i, j) in pairs]
"""
