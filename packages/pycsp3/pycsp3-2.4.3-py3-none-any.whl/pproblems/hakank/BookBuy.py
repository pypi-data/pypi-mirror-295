"""
From Martin Chlond Integer Programming Puzzles:

Four men, Peter and Paul and their sons Tom and Dick, buy books. When their
purchases are completed it turns out that each man has paid for each of his
books a number of dollars equal to the number of books he has bought. Each
family (father and son) has spent $65. Peter has bought one more book than
Tom, and Dick has bought only one book. Who is Dick's father?
"""

from pycsp3 import *

Peter, Paul = Fathers = range(2)
Tom, Dick = Sons = range(2)

# x[i] is the number of books (and price) bought by the ith father
x = VarArray(size=2, dom=range(1, 10))

# y[i] is the number of books (and price) bought by the ith son
y = VarArray(size=2, dom=range(1, 10))

# z is 1 iff Peter is Tom's father
z = Var(0, 1)

satisfy(

    # Dick buys one book
    y[Dick] == 1,

    # Peter buys one more book than Tom
    x[Peter] == y[Tom] + 1,

    # each family spends $65
    [
        x[0] * x[0] + z * y[0] * y[0] + (1 - z) * y[1] * y[1] == 65,
        x[1] * x[1] + (1 - z) * y[0] * y[0] + z * y[1] * y[1] == 65
    ]
)
