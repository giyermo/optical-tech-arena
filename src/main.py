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
    print("--------------------------------")
    edges = [int(x) for x in input().split()] #parse edges that fail
    scenario = copy.deepcopy(base_network) # copy base network
    broken_serv = []
    fixed_serv = []

    while edges[0] != -1:
        for edge in edges: # Delete edges that fail
            scenario.deactivate_edge(edge)
            if scenario.edges[edge]["services"] != []:
                for service in scenario.edges[edge]["services"]:
                    if scenario.services[service-1]["dead"] == False:   
                        broken_serv.append(service)
                    scenario.deactivate_service(service)

        print("broken services: ", broken_serv)

        for idx in broken_serv:
            print("redirecting service: ", idx)
            service = scenario.services[idx-1]
            if service["dead"] == False:
                redirect = scenario.redirect_broken_service(service)
                if redirect == None:
                    if idx not in broken_serv:
                        broken_serv.append(idx)
                    if idx in fixed_serv:
                        fixed_serv.remove(idx)
                else:
                    if idx not in fixed_serv:
                        fixed_serv.append(idx)
                    if idx in broken_serv:
                        broken_serv.remove(idx)
        
        print(len(fixed_serv), flush=True)
        print("fixed_serv: ", fixed_serv)

        for service in fixed_serv:
            print(service, len(scenario.services[service-1]["path"]), flush=True)

            output = []

            for edge in scenario.services[service-1]["path"]:
                start = scenario.services[service-1]["wavelengths"][0]
                end = scenario.services[service-1]["wavelengths"][1]
                output.extend([edge, start, end])
            print(*output, flush=True)

        print("broken_serv: ", broken_serv)

        broken_serv = []
        fixed_serv = []

        edges = [int(x) for x in input().split()] # set next batch of edges