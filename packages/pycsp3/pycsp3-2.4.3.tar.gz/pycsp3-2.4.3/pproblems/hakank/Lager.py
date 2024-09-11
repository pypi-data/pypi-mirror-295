"""
Stock Problem.
Lager is the Swedish word for "stock"
"""

from pycsp3 import *

initial_stock = 5
production_costs = [25, 36, 30]
stock_costs = [4, 3, 5]
demands = [10, 15, 12]
production_capacities = [20, 16, 10]
nPeriods = len(production_costs)

# x[t] is the production (number of manufactured products) at time t
x = VarArray(size=nPeriods, dom=lambda t: range(production_capacities[t] + 1))

# y[t] is the stock at time t
y = VarArray(size=nPeriods + 1, dom=range(200))

satisfy(
    y[0] == initial_stock,

    # computing stocks
    [y[t] + x[t] == demands[t] + y[t + 1] for t in range(nPeriods)]
)

minimize(
    # minimizing overall cost
    Sum(production_costs[t] * x[t] + stock_costs[t] * y[t + 1] for t in range(nPeriods))
)
