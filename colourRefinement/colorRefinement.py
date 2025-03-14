from graph_io import load_graph
from collections import Counter
import os
import glob
import time

def colour_refinement(graphs):
    colours = {}

    # Return a sorted list with neighbour colours of the vertex
    def get_neighbour_colours(vertex, colouring):
        neighbour_colours = []
        for neighbour in vertex.neighbours:
            neighbour_colours.append(colouring[neighbour])
        return sorted(neighbour_colours)

    # Creates new colouring based on previous one
    def refine_colours(graph, colouring):
        nonlocal colours
        new_colouring = {}
        last_colour = max(colours.values(), default=max(colouring.values()))
        partitions = 0
        # Assign new colours based on given colouring and neighbours colours
        for vertex in graph:
            neighbours_colours = tuple(get_neighbour_colours(vertex, colouring))
            if (colouring[vertex], neighbours_colours) not in colours:
                partitions += 1
                last_colour += 1
                colours[(colouring[vertex], neighbours_colours)] = last_colour
            new_colouring[vertex] = colours[(colouring[vertex], neighbours_colours)]
        partitions = len(set(new_colouring.values()))
        return new_colouring, partitions

    results = []

    # Process each graph
    for index, graph in enumerate(graphs):
        # Start assigning colour based on degree to all vertices
        colouring = {v: v.degree for v in graph.vertices}
        partitions = len(set(colouring.values()))
        i = 0
        
        # Iteratively refine the colouring
        while True:
            i += 1 
            new_colouring, new_partitions = refine_colours(graph, colouring)
            colouring = new_colouring

            # Stop iterations if the new colouring is the same as the previous one
            if new_partitions == partitions:
                break

            partitions = new_partitions

        # Check if graph is discrete
        discrete = len(set(colouring.values())) == len(graph.vertices)
        results.append((index, colouring, i, discrete))

    # Output the results
    isomorphic_graphs = {}
    for index, colouring, iterations, discrete in results:
        colour_sum = sum(colouring.values())
        freq_dict = dict(Counter(colouring.values()))
        colour_freq = dict(Counter(freq_dict.values()))
        colour_freq = dict(sorted(colour_freq.items()))
        key = (colour_sum, discrete, iterations)
        if key not in isomorphic_graphs:
            isomorphic_graphs[key] = ([],[colour_freq])
        isomorphic_graphs[key][0].append(index)
    
    # Print result
    #print("Sets of possibly isomorphic graphs:")
    #for colour_sum, indexes in isomorphic_graphs.items():
    #    print(f"{indexes} {colour_sum[2]} {'discrete' if colour_sum[1] else ''}")

    # Return output
    return [(indexes[0], indexes[1], colour_count[2], colour_count[1]) for colour_count, indexes in
            isomorphic_graphs.items()]


if __name__ == '__main__':
    dir = 'colourRefinement/SampleGraphsBasicColorRefinement/'
    grl_files = glob.glob(os.path.join(dir, "*.grl"))
    for file_path in grl_files:
        print(file_path)
        with open(file_path) as f:
            L = load_graph(f, read_list=True)
            graphs = L[0]
            start_time = time.perf_counter()
            result = colour_refinement(graphs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(result)
            print(f"Execution time: {execution_time:.4f} seconds")