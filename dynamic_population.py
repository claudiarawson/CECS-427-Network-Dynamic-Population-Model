import argparse
import os
import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulation Program for Cascade or COVID-19 Infection')
    parser.add_argument('graph_file', type=str, help='Path to Graph File')
    parser.add_argument('--action', choices=['cascade', 'covid'], required=True, help='Cascade or COVID-19')
    parser.add_argument('--initiator', type=str, required=True, help='Initial Nodes. Please Separate by Commas')
    parser.add_argument('--threshold', type=float, default=0.5, help='Threshold for Cascade Effect [0, 1]')
    parser.add_argument('--probability_of_infection', type=float, default=0.1, help='Probability of Infection, Used for COVID-19 Simulation')
    parser.add_argument('--lifespan', type=int, default=10, help='Lifespan of the Infected, in Days')
    parser.add_argument('--shelter', type=float, default=0.0, help='Proportion of the Population Sheltered [0, 1]')
    parser.add_argument('--vaccination', type=float, default=0.0, help='Proportion of the Population Vaccinated [0, 1]')
    parser.add_argument('--interactive', action='store_true', help='Plots Graph and Node States Every Round')
    parser.add_argument('--plot', action='store_true', help='Plots Number of New Infections per Day')
    return parser.parse_args()

def load_network(file_path):
    if not os.path.isfile(file_path):
        sys.exit(f"Error: File not found - {file_path}")
    graph = nx.read_gml(file_path, label="id")
    return graph.to_directed() if not graph.is_directed() else graph

def assign_states(graph, starters, vaccinated):
    state_map = {}
    for node in graph.nodes:
        if node in vaccinated:
            state_map[node] = "V"
        else:
            state_map[node] = "S"
    for node in starters:
        if state_map.get(node) == "S":
            state_map[node] = "I"
    return state_map

def simulate_cascade(graph, seeds, threshold, days, shelter, vaccinated, draw, layout):
    state = assign_states(graph, seeds, vaccinated)
    daily_infections = []

    if draw:
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))

    for day in range(days):
        infected_today = set()

        for node in graph.nodes:
            if state[node] != "S" or node in shelter or node in vaccinated:
                continue
            neighbors = list(graph.predecessors(node))
            if not neighbors:
                continue
            infected_neighbors = sum(1 for n in neighbors if state[n] == "I")
            if (infected_neighbors / len(neighbors)) >= threshold:
                infected_today.add(node)

        for node in infected_today:
            state[node] = "I"
        daily_infections.append(len(infected_today))

        if draw:
            display_graph(graph, state, layout, day, "Cascade", ax)

    if draw:
        plt.ioff()
        plt.show()

    return daily_infections, state

def simulate_covid(graph, seeds, infection_prob, days, shelter, vaccinated, draw, layout):
    state = assign_states(graph, seeds, vaccinated)
    recovery_days = {node: 0 for node in graph.nodes}
    daily_infections = []

    if draw:
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 6))

    for day in range(days):
        for node in graph.nodes:
            if state[node] == "I":
                recovery_days[node] += 1
                if recovery_days[node] >= days:
                    state[node] = "R"

        new_cases = set()
        for node in graph.nodes:
            if state[node] != "S" or node in shelter or node in vaccinated:
                continue
            for n in graph.predecessors(node):
                if state[n] == "I" and random.random() < infection_prob:
                    new_cases.add(node)
                    break

        for node in new_cases:
            state[node] = "I"
            recovery_days[node] = 0
        daily_infections.append(len(new_cases))

        if draw:
            display_graph(graph, state, layout, day, "COVID", ax)

    if draw:
        plt.ioff()
        plt.show()

    return daily_infections, state

def display_graph(graph, states, pos, day, title, axis):
    color_key = {"S": "blue", "I": "red", "R": "yellow", "V": "green"}
    node_colors = [color_key[states[node]] for node in graph.nodes]

    axis.clear()
    nx.draw(graph, pos=pos, node_color=node_colors, with_labels=True, ax=axis)
    axis.set_title(f"{title} Simulation - Day {day+1}")
    patches = [mpatches.Patch(color=v, label=k) for k, v in color_key.items()]
    axis.legend(handles=patches, loc="lower right")
    plt.draw()
    plt.pause(0.5)

def plot_results(infections, mode):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(infections) + 1), infections, marker="o")
    plt.title(f"New Infections Per Day - {mode}")
    plt.xlabel("Day")
    plt.ylabel("New Cases")
    plt.grid(True)
    plt.show()

def draw_final_state(graph, final_states, layout, mode):
    color_scheme = {"S": "blue", "I": "red", "R": "yellow", "V": "green"}
    colors = [color_scheme[final_states[n]] for n in graph.nodes]

    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos=layout, node_color=colors, with_labels=True)
    plt.title(f"Final Network State - {mode}")
    plt.legend(handles=[mpatches.Patch(color=v, label=k) for k, v in color_scheme.items()], loc="lower right")
    plt.show()

def main():
    random.seed(42)
    args = parse_arguments()
    G = load_network(args.graph_file)

    try:
        starter_nodes = [int(x.strip()) for x in args.initiator.split(",")]
        assert all(node in G.nodes for node in starter_nodes)
    except Exception:
        sys.exit(f"Invalid initiator(s). Choose from: {list(G.nodes)}")

    num_sheltered = int(args.shelter * G.number_of_nodes())
    num_vaccinated = int(args.vaccination * G.number_of_nodes())
    sheltered = set(random.sample(list(G.nodes), num_sheltered))
    vaccinated = set(random.sample(list(G.nodes), num_vaccinated))
    layout = nx.spring_layout(G)

    if args.action == "cascade":
        infections, states = simulate_cascade(
            G, starter_nodes, args.threshold, args.lifespan, sheltered, vaccinated, args.interactive, layout)
    else:
        infections, states = simulate_covid(
            G, starter_nodes, args.probability_of_infection, args.lifespan, sheltered, vaccinated, args.interactive, layout)

    if args.plot:
        plot_results(infections, args.action)
    draw_final_state(G, states, layout, args.action)

if __name__ == "__main__":
    main()
