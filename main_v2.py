import random
import time
from matplotlib import pyplot as plt
import json


class Graph:
    def __init__(self, color_dict):
        self.graph = {}
        self.color_dict = color_dict

    def add_vertex(self, vertex, color=-1):
        if vertex not in self.graph:
            self.graph[vertex] = {'color': color, 'neighbors': set()}

    def add_edge(self, v1, v2):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.graph[v1]['neighbors'].add(v2)
        self.graph[v2]['neighbors'].add(v1)

    def get_vertices(self):
        return list(self.graph.keys())

    def get_edges(self):
        edges = []
        for v in self.graph:
            for neighbor in self.graph[v]['neighbors']:
                if (v, neighbor) not in edges and (neighbor, v) not in edges:
                    edges.append((v, neighbor))
        return edges

    def get_vertex_color(self, vertex):
        return self.graph[vertex]['color']

    def get_vertex_color_code(self, vertex):
        return self.color_dict[self.graph[vertex]['color']]

    def get_neighbors(self, vertex):
        return list(self.graph[vertex]['neighbors'])

    def get_vertex(self, vertex):
        return self.graph.get(vertex)

    def set_vertex_color(self, vertex, color):
        vertex_attrs = self.get_vertex(vertex)
        if vertex_attrs is not None:
            vertex_attrs['color'] = color
        else:
            print(f"Vertex {vertex} not found in graph.")

    def get_unique_colors(self):
        unique_colors = set()
        for vertex in self.graph:
            vertex_attrs = self.get_vertex(vertex)
            if vertex_attrs is not None and 'color' in vertex_attrs:
                unique_colors.add(vertex_attrs['color'])
        return list(unique_colors)


def parse_int_keys(pairs):
    return {int(key): value for key, value in pairs}


def init_color_dict():
    # Open the file for reading and load the dictionary from JSON
    with open('color_dict.json', 'r') as file:
        color_dict = json.load(file, object_pairs_hook=parse_int_keys)

    return color_dict


def init_graph(node_index, color_dict):
    # Create an empty undirected graph
    graph = Graph(color_dict)
    # Add the first node to the graph
    graph.add_vertex(node_index, color=0)
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
    neighbors = list(graph.get_neighbors(node))

    color_list = []
    # Check the color label of each neighboring node
    for neighbor in neighbors:
        color = graph.get_vertex_color(neighbor)
        color_list.append(color)

    # Find lowest-numbered color
    color = find_min_color(color_list, color_dict)
    graph.set_vertex_color(node, color)


def print_statistic(graph, d):
    color_number = len(graph.get_unique_colors())
    print(f'Number of nodes: {len(graph.get_vertices())}, {d}-inductive, Number of color: {color_number}')

    return color_number


def run_simulation(inductive, node_number, color_dict, step_plot=False, plot_name=""):
    graph, node_index = init_graph(node_number, color_dict)
    if step_plot:
        print(f"Step {node_number - node_index}", graph.graph)

    while node_index > 0:
        # Adversary input
        # Add the new node to the graph with additional string attribute
        graph.add_vertex(node_index)
        # Add d random edges to the new node
        for j in range(inductive):
            # Choose a random node from the existing nodes
            nodes = list(graph.get_vertices())
            nodes.remove(node_index)
            node = random.choice(nodes)
            # Add an undirected edge between the new node and the existing node
            graph.add_edge(node_index, node)

        # First fit coloring
        first_fit(graph, node_index, color_dict)
        node_index -= 1

        if step_plot:
            print(f"Step {node_number - node_index}", graph.graph)

    return graph


def sample_experiment(color_dict):
    node_index = 10
    d = 2
    graph = run_simulation(d, node_index, color_dict, step_plot=True, plot_name="./plots/10_nodes_2_inductive")
    print_statistic(graph, d)


def experiment1(color_dict):
    plt.clf()
    d = 5
    colors = []
    start = 100
    end = 10001
    step = 100
    times = []
    total_start_time = time.time()
    for node_number in range(start, end, step):
        start_time = time.time()
        graph = run_simulation(d, node_number, color_dict)
        # if node_number == start:
        #     plot_graph(graph, d)
        color_stats = print_statistic(graph, d)
        colors.append(color_stats)  # append the number of unique colors
        end_time = time.time()
        times.append(end_time - start_time)
    total_end_time = time.time()
    print('Elapsed times:', total_end_time - total_start_time)

    # plot node_number vs number of unique colors
    plt.figure(1)
    plt.plot(list(range(start, end, step)), colors)
    plt.xlabel('Node number')
    plt.ylabel('Number of colors')
    plt.title('Experiment 1')

    # plot node_number vs elapsed time
    plt.figure(2)
    plt.plot(list(range(start, end, step)), times)
    plt.xlabel('Node number')
    plt.ylabel('Elapsed time (seconds)')
    plt.title('Experiment 1')

    # save the plots as PNG files
    plt.figure(1).savefig('./plots/experiment1_color_plot.png')
    plt.figure(2).savefig('./plots/experiment1_time_plot.png')


def experiment2(color_dict):
    plt.clf()
    d = 500
    node_number = 1000
    colors = []
    times = []
    total_start_time = time.time()
    for inductive in range(2, d):
        start_time = time.time()
        graph = run_simulation(inductive, node_number, color_dict)
        # if node_number == start:
        #     plot_graph(graph, d)
        color_stats = print_statistic(graph, inductive)
        colors.append(color_stats)  # append the number of unique colors
        end_time = time.time()
        times.append(end_time - start_time)
    total_end_time = time.time()
    print('Elapsed times:', total_end_time - total_start_time)

    # plot inductive vs number of unique colors
    plt.figure(1)
    plt.plot(list(range(2, d)), colors)
    plt.xlabel('d-inductive')
    plt.ylabel('Number of colors')
    plt.title('Experiment 2')

    # plot inductive vs elapsed time
    plt.figure(2)
    plt.plot(list(range(2, d)), times)
    plt.xlabel('d-inductive')
    plt.ylabel('Elapsed time (seconds)')
    plt.title('Experiment 2')

    # save the plots as PNG files
    plt.figure(1).savefig('./plots/experiment2_color_plot.png')
    plt.figure(2).savefig('./plots/experiment2_time_plot.png')


def experiment3(color_dict):
    plt.clf()
    d_max = 99
    node_numbers = [500, 1000, 2000]
    colors_all = []

    for node_number in node_numbers:
        colors = []
        for inductive in range(1, d_max+1):
            graph = run_simulation(inductive, node_number, color_dict)
            color_stats = print_statistic(graph, inductive)
            colors.append(color_stats)
        colors_all.append(colors)

    plt.figure()
    for i, node_number in enumerate(node_numbers):
        plt.plot(list(range(1, d_max+1)), colors_all[i], label=f"{node_number} nodes")
    plt.xlabel("d-inductive")
    plt.ylabel("Number of unique colors")
    plt.legend()
    plt.title("Experiment 3")
    plt.savefig('./plots/experiment3_color_plot.png')


def main():
    color_dict = init_color_dict()

    # run with 10 nodes, 2-inductive graph for correctness checking
    print("sample_experiment: run with 10 nodes, 2-inductive graph for correctness checking")
    sample_experiment(color_dict)

    # 5-inductive graph, with nodes 10, 20, ...  10000
    print("experiment1: 5-inductive graph, with nodes 10, 20, ...  10000")
    experiment1(color_dict)

    # 1000 nodes, inductive from 2...500
    print("experiment2: 1000 nodes, inductive from 2...500")
    experiment2(color_dict)

    # 100 nodes, 1000 nodes, 2000 nodes run on inductive from 1 to 80
    print("experiment3: 100 nodes, 1000 nodes, 2000 nodes run on inductive from 1 to 80")
    experiment3(color_dict)


if __name__ == "__main__":
    main()

