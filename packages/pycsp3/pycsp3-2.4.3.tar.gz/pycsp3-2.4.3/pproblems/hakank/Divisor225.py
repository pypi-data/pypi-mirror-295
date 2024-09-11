"""
What is the smallest number divisible by 225 that consists of all 1s and 0s?

Out of natural numbers, the answer is trivially 0.
So trivially that clearly you actually care about positive integers instead.
Out of those, the answer is 11111111100 (nine ones and then two zeros).

Reasoning: 225 = 25 * 9.
Thus, every multiple of 225 is a multiple of 25, and its last digits will be either 00, 25, 50, or 75,
according as to the multiplying factor's residue modulo 4.
Out of these, only the first is acceptable, so we must multiply 225 by a multiple of 4, which is to multiply 9 by a multiple of 100.
Thus, the problem reduces to the smallest multiple of 9 which is all 1s and 0s, with two zeros tacked onto the end.
As is well known, to be a multiple of 9 is to have digits which add up to a multiple of 9
(by consideration of the fact that 10 = 1 modulo 9); thus, the smallest (positive) answer is nine ones followed by two zeros.
"""
from pycsp3 import *

n = data or 11

# x[i] is the ith digit of the original number
x = VarArray(size=n, dom={0, 1})

y = Var(range(1, 100_000_000))

satisfy(
    x * [10 ** (n - 1 - i) for i in range(n)] == y * 225
)

"""
1) can be tackled by picat (but not ACE for the moment)
"""
