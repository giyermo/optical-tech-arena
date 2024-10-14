import copy
from constants import *
from network import *
from parser import *
from scenario_maker import *

# Parse the network
nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)

scenarios = produce_scenarios(edges)
print_scenarios(scenarios)
print(base_network.nodes)

scenarios_no = int(input()) # Number of scenarios provided by the environment

for _ in range(scenarios_no): # For each scenario
    
    edges = [int(x) for x in input().split()] #parse edges that fail
    scenario = copy.deepcopy(base_network) # copy base network

    while edges[0] != -2:
        for edge in edges: # Delete edges that fail
            scenario.delete_edge(edge)

        scenario.solve_scenario(base_network)
        
        edges = [int(x) - 1 for x in input().split()] # set next batch of edges