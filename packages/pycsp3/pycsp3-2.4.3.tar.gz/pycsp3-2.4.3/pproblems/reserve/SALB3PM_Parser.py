from pycsp3.problems.data.parsing import *

print("ok")
n = number_in(line())
data['durations'] = [number_in(next_line()) for _ in range(n)]
pr = []
while True:
    t = numbers_in(next_line())
    assert len(t) == 2
    if t[0] == -1:
        assert t[1] == -1
        break
    pr.append(decrement(t))
data['precedences'] = pr
