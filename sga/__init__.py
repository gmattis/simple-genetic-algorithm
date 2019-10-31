# ToDo: More explicit variables names
# ToDo: Show more statistics about generations
# ToDo: Write a real introduction for all the scripts
# ToDo: Add a license
# ToDo: Adapt GENE_PROB_FACT, NODE_PROB_FACT and AMP_MUT_FACT to take account of the fitness
# ToDo: Verify the settings are correct when loading a state
# ToDo: Fix the XOR example

try:
    from graphviz import Digraph
except ImportError:
    print("It seems that the Graphviz library is not installed. "
          "You won't be able to display the neural network of individuals.")
    import time
    time.sleep(1)
    del time
