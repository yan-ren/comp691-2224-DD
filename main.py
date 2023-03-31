import random
import time

import networkx as nx
from matplotlib import pyplot as plt
import json


# Define a function to parse key-value pairs with integer keys
def parse_int_keys(pairs):
    return {int(key): value for key, value in pairs}


def init_color_dict():
    # Open the file for reading and load the dictionary from JSON
    with open('color_dict.json', 'r') as file:
        color_dict = json.load(file, object_pairs_hook=parse_int_keys)

    return color_dict


def init_graph(node_index):
    # Create an empty undirected graph
    graph = nx.Graph()
    # Add the first node to the graph
    graph.add_node(node_index, color=0)
    node_index -= 1

    return graph, node_index


# Find the minimum integer in the range that is not in the list
def find_min_color(color_list, color_dict):
    for color in range(0, len(color_dict) + 1):
        if color not in color_list:
            return color

    return Exception("Run out of color!")


def first_fit(graph, node, color_dict):
    # Get all neighbors of node
    neighbors = list(graph.neighbors(node))

    color_list = []
    # Check the color label of each neighboring node
    for neighbor in neighbors:
        if 'color' in graph.nodes[neighbor]:
            color = graph.nodes[neighbor]['color']
            color_list.append(color)

    # Find lowest-numbered color
    color = find_min_color(color_list, color_dict)
    nx.set_node_attributes(graph, {node: color}, 'color')


def plot_graph(graph, inductive, show_figure=False, save_figure=False):
    # Create a list of node colors that match the order of the nodes in the graph
    node_colors = [graph.nodes[n]['color'] for n in graph.nodes()]
    # Draw the graph with the node colors based on the color labels
    nx.draw(graph, node_color=node_colors, with_labels=True)
    if save_figure:
        plt.savefig(f'./plots/{len(graph.nodes())}_nodes_{inductive}_inductive.png')
    # Show the plot
    if show_figure:
        plt.show()


def print_statistic(graph):
    node_colors = [graph.nodes[n]['color'] for n in graph.nodes()]
    color_number = len(set(node_colors))
    print(f'Number of nodes: {len(graph.nodes())}, Number of color: {color_number}')

    return color_number


def run_simulation(inductive, node_number, color_dict):
    graph, node_index = init_graph(node_number)

    while node_index > 0:
        # Adversary input
        # Add the new node to the graph with additional string attribute
        graph.add_node(node_index)
        # Add d random edges to the new node
        for j in range(inductive):
            # Choose a random node from the existing nodes
            nodes = list(graph.nodes())
            nodes.remove(node_index)
            node = random.choice(nodes)
            # Add an undirected edge between the new node and the existing node
            graph.add_edge(node_index, node)

        # First fit coloring
        first_fit(graph, node_index, color_dict)
        node_index -= 1

    return graph


def sample_experiment(color_dict):
    node_index = 10
    d = 2
    graph = run_simulation(d, node_index, color_dict)
    print_statistic(graph)
    plot_graph(graph, d, save_figure=True)


def experiment1(color_dict):
    d = 5
    colors = []
    start = 1000
    end = 100001
    step = 1000
    times = []
    total_start_time = time.time()
    for node_number in range(start, end, step):
        start_time = time.time()
        graph = run_simulation(d, node_number, color_dict)
        color_stats = print_statistic(graph)
        colors.append(color_stats)  # append the number of unique colors
        end_time = time.time()
        times.append(end_time - start_time)
    total_end_time = time.time()
    print('Elapsed times:', total_end_time - total_start_time)

    # plot node_number vs number of unique colors
    plt.figure(1)
    plt.plot(range(start, end, step), colors)
    plt.xlabel('Node number')
    plt.ylabel('Number of colors')
    plt.title('Experiment 1')

    # plot node_number vs elapsed time
    plt.figure(2)
    plt.plot(range(start, end, step), times)
    plt.xlabel('Node number')
    plt.ylabel('Elapsed time (seconds)')
    plt.title('Experiment 1')

    # save the plots as PNG files
    plt.figure(1).savefig('./plots/experiment1_color_plot.png')
    plt.figure(2).savefig('./plots/experiment1_time_plot.png')


def main():
    color_dict = init_color_dict()

    # run with ten nodes, 2-inductive graph for correctness checking
    sample_experiment(color_dict)

    # 2-inductive graph, with nodes 10, 20, ...  1000
    # experiment1(color_dict)


if __name__ == "__main__":
    main()

