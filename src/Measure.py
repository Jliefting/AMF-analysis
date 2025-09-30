import numpy as np

def measure_length_um_edge(edge, G):
    #TO UPDATE
    pixel_conversion_factor = 2.07 #um.pixel
    #TO UPDATE
    length_edge = 0
    edge_data = G.get_edge_data(edge[0], edge[1])  # Assumes edge is a tuple (node1, node2)
    pixels = edge_data['pixel_list']  # Access the pixel list attribute
    for i in range(len(pixels) // 10 + 1):
        if i * 10 <= len(pixels) - 1:
            length_edge += np.linalg.norm(
                np.array(pixels[i * 10])
                - np.array(pixels[min((i + 1) * 10, len(pixels) - 1)])
            )
    return length_edge * pixel_conversion_factor

def get_length_tot(G):
    length = 0
    lengths_list = []
    for edge in G.edges:
        length += measure_length_um_edge(edge, G)
        lengths_list.append(length)
    return (length), lengths_list
    
def divide_branches(G):
    # Initialize dictionaries to store the edges
    tip_branches = []
    non_tip_branches = []

    # Iterate through all edges in the graph
    for edge in G.edges:
        # Get the nodes connected by the edge
        node1, node2 = edge
        
        # Get the degrees of both nodes
        degree1 = G.degree[node1]
        degree2 = G.degree[node2]
        
        # Check if the edge connects to a tip node (degree 1)
        if degree1 == 1 or degree2 == 1:
            tip_branches.append(edge)
        else:
            non_tip_branches.append(edge)

    return tip_branches, non_tip_branches

def calculate_branch_lengths(G):
    # Divide the graph into tip and non-tip branches
    tip_branches, non_tip_branches = divide_branches(G)

    # Initialize length attributes
    tip_length = 0
    non_tip_length = 0

    # Store individual edge lengths in the graph
    for edge in tip_branches:
        edge_length = measure_length_um_edge(edge, G)
        G.edges[edge]["length_um"] = edge_length
        tip_length += edge_length

    for edge in non_tip_branches:
        edge_length = measure_length_um_edge(edge, G)
        G.edges[edge]["length_um"] = edge_length
        non_tip_length += edge_length

    # Store total lengths as graph attributes
    G.graph["tip_total_length_um"] = tip_length
    G.graph["non_tip_total_length_um"] = non_tip_length

    return G  # Return the updated graph object

def get_tip_branch_lengths(G):
    tip_lengths = []
    
    # Iterate over edges and collect lengths of tip branches
    for edge in G.edges:
        if "length_um" in G.edges[edge]:  # Ensure length is stored
            edge_length = G.edges[edge]["length_um"]
            if edge in divide_branches(G)[0]:  # Check if edge is a tip branch
                tip_lengths.append(edge_length)
    
    return tip_lengths

def get_non_tip_branch_lengths(G):
    non_tip_lengths = []

    # Get non-tip branches from divide_branches
    _, non_tip_branches = divide_branches(G)

    # Iterate over edges and collect lengths of non-tip branches
    for edge in G.edges:
        if "length_um" in G.edges[edge]:  # Ensure length is stored
            edge_length = G.edges[edge]["length_um"]
            if edge in non_tip_branches:
                non_tip_lengths.append(edge_length)

    return non_tip_lengths