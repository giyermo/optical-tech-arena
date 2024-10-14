from constants import *
from network import *
from parser import *
from scenario_maker import *

# Parse the network
nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)

scenarios = produce_scenarios(edges)
print_scenarios(scenarios)

scenarios_no = int(input()) # Number of scenarios provided by the environment

for _ in range(scenarios_no): # For each scenario
    
    edges = [int(x) for x in input().split()] #parse edges that fail
    scenario = copy.deepcopy(base_network) # copy base network

    while edges[0] != -1:
        for edge in edges: # Delete edges that fail
            scenario.deactivate_edge(edge)
            if scenario.edges[edge]["services"] != []:
                for service in scenario.edges[edge]["services"]:
                    scenario.deactivate_service(service-1)

        scenario.solve_scenario(base_network)
        
        edges = [int(x) for x in input().split()] # set next batch of edges