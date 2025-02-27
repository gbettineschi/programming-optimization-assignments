import pulp as pl


def ex1():
    retval = {}
    retval["x"] = None
    retval["y"] = None
    retval["obj"] = None
    retval["tight_constraints"] = [None]

    problem = pl.LpProblem("ex1", pl.LpMinimize)
    x = pl.LpVariable("x")
    y = pl.LpVariable("y")

    problem += x >= -10
    problem += y <= 10
    problem += 3 * x + 2 * y <= 10
    problem += 12 * x + 14 * y >= -12.5
    problem += 2 * x + 3 * y >= 3
    problem += 5 * x - 6 * y >= -100

    problem += 122 * x + 143 * y
    problem.solve(pl.PULP_CBC_CMD(msg=False))

    retval["x"] = pl.value(x)
    retval["y"] = pl.value(y)
    retval["obj"] = pl.value(problem.objective)
    retval["tight_constraints"] = [
        i
        for i, constraint in enumerate(problem.constraints.values(), start=1)
        if abs(constraint.slack) < 1e-6
    ]

    return retval


def ex2():
    retval = {}
    retval["x1"] = None
    retval["x2"] = None
    retval["x3"] = None
    retval["x4"] = None
    retval["x5"] = None
    retval["x6"] = None
    retval["obj"] = None

    choices = range(1, 7)

    def payoff(i, j):
        if i == j:
            return 0
        elif i - j == 1:
            return -2
        elif i - j == -1:
            return 2
        elif i > j:
            return 1
        else:
            return -1

    problem = pl.LpProblem("ex2", pl.LpMaximize)
    strategy = pl.LpVariable.dicts("x", choices, lowBound=0)
    obj = pl.LpVariable("obj")

    # constrain probabilites to sum to 1
    problem += pl.lpSum(strategy.values()) == 1

    # constrain obj to be the minimum payoff of strategy, i.e. the payoff assuming a rational competitor
    for j in choices:
        problem += obj <= pl.lpSum(strategy[i] * payoff(i, j) for i in choices)

    problem += obj
    problem.solve(pl.PULP_CBC_CMD(msg=False))

    for k, v in strategy.items():
        retval[f"x{k}"] = pl.value(v)
    retval["obj"] = pl.value(obj)

    return retval


def ex3():
    retval = {}
    retval["obj"] = None
    retval["x1"] = None

    companies = range(1, 70)
    contracts = []
    with open("assignment1/hw1-03.txt", "r") as f:
        for line in f:
            if l := line.strip():
                i, j = map(int, l.split())
                contracts.append((i, j))

    # initialize LP relaxation of the integer problem assuming an integral solution
    problem = pl.LpProblem("ex3", pl.LpMinimize)
    delegations = pl.LpVariable.dicts("x", companies, lowBound=0)

    for i, j in contracts:
        problem += delegations[i] + delegations[j] >= 2

    problem += pl.lpSum(delegations.values())
    problem.solve(pl.PULP_CBC_CMD(msg=False))

    for i in companies:
        retval[f"x{i}"] = pl.value(delegations[i])
    retval["obj"] = pl.value(problem.objective)

    return retval


if __name__ == "__main__":
    print(ex3())
