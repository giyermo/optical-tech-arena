import random

def produce_scenarios(edges):
    """
    Produce failure scenarios

    Naive version, with random failures

    Parameters
    ----------
    edges : list
        List of edges of the graph

    Returns
    -------
    list
        List of lists of edges that fail in each scenario
    """
    scenarios_no = 1# random.randint(1, T_1_MAX)
    scenarios = []
    for scenario in range(scenarios_no):
        scenario_edges = []
        failures = 1#random.randint(1, min(int(len(edges)/3), T_2_MAX))
        for _ in range(failures):
            edge = random.randint(0, len(edges)-1)
            if edge not in scenario_edges:
                scenario_edges.append(edge)
        if scenario_edges not in scenarios:
            scenarios.append(scenario_edges)
    return scenarios

def print_scenarios(scenarios:list):
    """
    Print failure scenarios to the standard output

    The first line contains the number of failure scenarios.
    The following lines describe each scenario, with the first number being
    the number of edges that fail, and the following numbers the indices of
    the edges that fail, counted from 1.
    """
    print(len(scenarios), flush=True)
    for scenario in scenarios:
        print(len(scenario), flush=True)
        # Edges should be counted from 1
        print(*[edge + 1 for edge in scenario], flush=True)