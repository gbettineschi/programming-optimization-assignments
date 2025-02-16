from pulp import *

def ex1():
    retval = {}
    retval["x"] = None
    retval["y"] = None
    retval["obj"] = None
    retval["tight_constraints"] = [ None ]

    problem = LpProblem("exercise1", LpMinimize)

    x = LpVariable("x", lowBound=-10)
    y = LpVariable("y", upBound=10)
    
    problem += (3*x + 2*y <= 10)
    problem += (12*x + 14*y >= -12.5)
    problem += (2*x + 3*y >= 3)
    problem += (5*x - 6*y >= -100)
    
    problem += 122 * x + 143 * y

    problem.solve(PULP_CBC_CMD(msg=False))

    retval["x"] = value(x)
    retval["y"] = value(y)
    retval["obj"] = value(problem.objective)
    retval["tight_constraints"] = [ i for i, constraint in enumerate(problem.constraints.values()) if abs(constraint.slack) < 1e-6 ]
    
    return retval

def ex2():
    retval = {}
    retval['x1'] = None
    retval['x2'] = None
    retval['x3'] = None
    retval['x4'] = None
    retval['x5'] = None
    retval['x6'] = None
    retval['obj'] = None
    # Insert your code below:


    # return retval dictionary
    return retval


def ex3():
    retval = {}
    retval['obj'] = None
    retval['x1'] = None
    # there should be retval['xi'] for each company number i
    # Insert your code below:


    # return retval dictionary
    return retval


if __name__ == "__main__":
    print(ex1())