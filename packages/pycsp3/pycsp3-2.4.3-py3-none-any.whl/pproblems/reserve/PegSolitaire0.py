"""
See https://www.cs.york.ac.uk/aig/projects/implied/docs/CPAIOR03.pdf
English style (standard), 33 holes

With time as third component, instances are easy to be solved with default solver parameters
contrary to PegSolitaire1

PegSolitaire0-english-dec2-4-4-0.xml  in 31s
PegSolitaire0-english-dec2-3-3-0.xml -pra=0 -ale=4 in 3s

python ppycsp3/pproblems/reserve/PegSolitaire0.py -data=[4,4,0] -variant=english-dec2
"""

from pycsp3 import *

from PegSolitaire_Generator import generate_boards

assert variant() in {"english", "french", "3x3", "4x4", "test1", "test2"} and subvariant() in ("dec1", "dec2", "hybrid")

origin_x, origin_y, nMoves = data

init_board, final_board = generate_boards(variant(), origin_x, origin_y)
n, m = len(init_board), len(init_board[0])

horizon = sum(sum(v for v in row if v) for row in init_board) - sum(sum(v for v in row if v) for row in final_board)
nMoves = horizon if nMoves <= 0 or horizon < nMoves else nMoves
assert 0 < nMoves <= horizon

pairs = [(i, j) for i in range(n) for j in range(m) if init_board[i][j] is not None]
_m = [[(i, j, i + 1, j, i + 2, j), (i, j, i, j + 1, i, j + 2), (i, j, i - 1, j, i - 2, j), (i, j, i, j - 1, i, j - 2)] for i, j in pairs]
transitions = sorted(t for row in _m for t in row if 0 <= t[4] < n and 0 <= t[5] < m and init_board[t[4]][t[5]] is not None)
nTransitions = len(transitions)

# x[i,j,t] is the value at row i and column j at time t
x = VarArray(size=[n, m, nMoves + 1], dom={0, 1})

# y[t] is the move (transition) performed at time t
y = VarArray(size=nMoves, dom=range(nTransitions))

satisfy(
    # setting the initial board
    x[:, :, 0] == init_board,

    # setting the final board
    x[:, :, -1] == final_board
)

if subvariant() in ("dec1", "dec2"):

    def unchanged(i, j, t):
        valid = [k for k, tr in enumerate(transitions) if (i, j) in (tr[0:2], tr[2:4], tr[4:6])]
        if len(valid) == 0:
            return None
        return iff(y[t] not in valid if subvariant("dec1") else conjunction(y[t] != k for k in valid), x[i][j][t] == x[i][j][t + 1])


    def to0(i, j, t):
        valid = [k for k, tr in enumerate(transitions) if (i, j) in (tr[0:2], tr[2:4])]
        if len(valid) == 0:
            return None
        return iff(y[t] in valid if subvariant("dec1") else disjunction(y[t] == k for k in valid), (x[i][j][t] == 1) & (x[i][j][t + 1] == 0))


    def to1(i, j, t):
        valid = [k for k, tr in enumerate(transitions) if (i, j) == tr[4:6]]
        if len(valid) == 0:
            return None
        return iff(y[t] in valid if subvariant("dec1") else disjunction(y[t] == k for k in valid), (x[i][j][t] == 0) & (x[i][j][t + 1] == 1))


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
            t = [ANY if init_board[i][j] is None else 1 if tr[0:2] == (i, j) or tr[2:4] == (i, j) else 0 if tr[4:6] == (i, j) else ANY
                 for i in range(n) for j in range(m)]
            # secondly, x[t+1,i,j]
            t += [ANY if init_board[i][j] is None else 0 if tr[0:2] == (i, j) or tr[2:4] == (i, j) else 1 if tr[4:6] == (i, j) else eq(col(i * m + j))
                  for i in range(n) for j in range(m)]
            # lastly, the transition (move)
            t.append(k)
            tbl.append(tuple(t))
        return tbl


    T = table()

    satisfy(
        (x[:, :, t], x[:, :, t + 1], y[t]) in T for t in range(nMoves - 1)
    )
