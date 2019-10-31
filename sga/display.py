import numpy as np

from .config import Config
from .individual import Individual


def display_genome(individual: Individual, config: Config, display=True):
    """ Displays the neural network of an individual """
    total_nodes = config.IND_INP_NUMBER + config.IND_MAX_NODES + config.IND_OUT_NUMBER

    try:
        from graphviz import Digraph
    except ImportError:
        print("An error occured while importing Graphviz. You should check if you have installed it.")
        return

    dot = Digraph(name="best_individual", format="png", graph_attr={"rankdir": "LR", "splines": "spline"})

    input_dot = Digraph(name="input_subgraph", graph_attr={"rank": "min"})
    for node in range(config.IND_INP_NUMBER):
        input_dot.node(str(node), str(node), color='blue')

    hidden_dot = Digraph(name="hidden_subgraph")
    for node in range(config.IND_INP_NUMBER, config.IND_INP_NUMBER + config.IND_MAX_NODES):
        if (individual.genes[node] != np.inf).any():
            hidden_dot.node(str(node), str(node))
            for from_node in range(total_nodes):
                if individual.genes[node][from_node] != np.inf:
                    dot.edge(str(from_node), str(node), label=str(round(individual.genes[node][from_node], 3)))

    output_dot = Digraph(name="output_subgraph", graph_attr={"rank": "max"})
    for node in range(config.IND_INP_NUMBER + config.IND_MAX_NODES, total_nodes):
        output_dot.node(str(node), str(node), color='red')
        for from_node in range(total_nodes):
            if individual.genes[node][from_node] != np.inf:
                dot.edge(str(from_node), str(node), label=str(round(individual.genes[node][from_node], 3)))

    dot.subgraph(input_dot)
    dot.subgraph(hidden_dot)
    dot.subgraph(output_dot)
    dot.render(view=display)
