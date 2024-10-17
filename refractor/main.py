#!/usr/bin/env python3
from service import Service
from scenario_parser import *
from scenario_maker import *
from network import Network
from functions import *
import copy

nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)

# scenarios = produce_scenarios(edges)
# print_scenarios(scenarios)

print("1", flush=True)
print("1", flush=True)
print("1", flush=True)


n_scenarios = int(input())


for _ in range(n_scenarios):
    scenario = copy.deepcopy(base_network)

    continuee = True

    while continuee:
        line = input()

        if line == "-1":
            continuee = False
        else:
            edges_ids = [int(x) for x in line.split()]

            redirected_services, scenario = process_scenario(scenario, edges_ids)

            print(len(redirected_services), flush=True)
            for service in redirected_services:
                print(service, len(scenario.services[service].path), flush=True)
                path = scenario.services[service].path
                wavelengths = scenario.services[service].wavelengths
                stuff = []
                for edge, (w_start, w_end) in zip(path, wavelengths):
                    stuff.extend([edge, w_start, w_end])

                print(*stuff, flush=True)
