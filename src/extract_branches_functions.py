import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas 


def extract_branches(doc_skel):
    def get_neighbours(pixel):
        x = pixel[0]
        y = pixel[1]
        primary_neighbours = {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}
        secondary_neighbours = {
            (x + 1, y - 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
        }
        num_neighbours = 0
        actual_neighbours = []
        for neighbour in primary_neighbours:
            if neighbour in non_zero_pixel:
                num_neighbours += 1
                xp = neighbour[0]
                yp = neighbour[1]
                primary_neighboursp = {
                    (xp + 1, yp),
                    (xp - 1, yp),
                    (xp, yp + 1),
                    (xp, yp - 1),
                }
                for neighbourp in primary_neighboursp:
                    secondary_neighbours.discard(neighbourp)
                actual_neighbours.append(neighbour)
        for neighbour in secondary_neighbours:
            if neighbour in non_zero_pixel:
                num_neighbours += 1
                actual_neighbours.append(neighbour)
        return (actual_neighbours, num_neighbours)

    pixel_branch_dic = {pixel: set() for pixel in doc_skel.keys()}
    is_node = {pixel: False for pixel in doc_skel.keys()}
    pixel_set = set(doc_skel.keys())
    non_zero_pixel = doc_skel
    new_index = 1
    non_explored_direction = set()

    # Tip tracking
    tip_pixels = set()  # To store tip pixels
    tip_branches = {}  # To store branch lengths for tip branches

    # Create an image with the same size as the input
    max_x = max(p[0] for p in doc_skel.keys())
    max_y = max(p[1] for p in doc_skel.keys())
    image = np.zeros((max_x + 1, max_y + 1), dtype=int)

    while len(pixel_set) > 0:
        is_new_start = len(non_explored_direction) == 0
        if is_new_start:
            pixel = pixel_set.pop()
        else:
            pixel = non_explored_direction.pop()

        actual_neighbours, num_neighbours = get_neighbours(pixel)

        if is_new_start:
            if num_neighbours == 2:
                new_index += 1
                pixel_branch_dic[pixel] = {new_index}

        is_node[pixel] = num_neighbours in [0, 1, 3, 4]
        pixel_set.discard(pixel)

        # Update the image with the number of neighbors for each pixel
        image[pixel[0], pixel[1]] = num_neighbours

        #!!! This is to solve the two neighbours nodes problem
        if is_node[pixel]:
            for neighbour in actual_neighbours:
                if is_node[neighbour]:
                    new_index += 1
                    pixel_branch_dic[pixel].add(new_index)
                    pixel_branch_dic[neighbour].add(new_index)
            continue
        else:
            for neighbour in actual_neighbours:
                if neighbour in pixel_set:
                    non_explored_direction.add(neighbour)
                pixel_branch_dic[neighbour] = pixel_branch_dic[neighbour].union(pixel_branch_dic[pixel])

    # Identify tip pixels and their branches
    for pixel, branches in pixel_branch_dic.items():
        actual_neighbours, num_neighbours = get_neighbours(pixel)
        if num_neighbours == 1:  # Tip pixels
            tip_pixels.add(pixel)
            # For each tip pixel, we take one branch (there could be multiple, but we choose the first)
            branch_id = list(branches)[0]
            if branch_id not in tip_branches:
                # Calculate the length of the branch (number of pixels in the branch)
                branch_pixels = [p for p, b in pixel_branch_dic.items() if branch_id in b]
                tip_branches[branch_id] = len(branch_pixels)  # Store branch length

    return pixel_branch_dic, is_node, new_index, tip_pixels, tip_branches, image
    
def get_neighbours2(pixel, xs, ys):
    x = pixel[0]
    y = pixel[1]
    primary_neighbours = {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}
    secondary_neighbours = {
        (x + 1, y - 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x - 1, y - 1),
    }
    pixel_list = [(x, ys[i]) for i, x in enumerate(xs)]
    num_neighbours = 0
    actual_neighbours = set()
    for neighbour in primary_neighbours:
        if neighbour in pixel_list:
            xp = neighbour[0]
            yp = neighbour[1]
            primary_neighboursp = {
                (xp + 1, yp),
                (xp - 1, yp),
                (xp, yp + 1),
                (xp, yp - 1),
            }
            for neighbourp in primary_neighboursp:
                secondary_neighbours.discard(neighbourp)
            actual_neighbours.add(neighbour)
    for neighbour in secondary_neighbours:
        if neighbour in pixel_list:
            actual_neighbours.add(neighbour)
    return actual_neighbours

def from_sparse_to_graph(doc_skel):
    column_names = ["origin", "end", "pixel_list"]
    graph = pd.DataFrame(columns=column_names)
    pixel_branch_dic, is_node, new_index, tip_pixels, tip_branches, neighbour_img = extract_branches(doc_skel)
    nodes = []
    edges = {}
    for pixel in pixel_branch_dic:
        for branch in pixel_branch_dic[pixel]:
            right_branch = branch
            if right_branch not in edges.keys():
                edges[right_branch] = {"origin": [], "end": [], "pixel_list": [[]]}
            if is_node[pixel]:
                if len(edges[right_branch]["origin"]) == 0:
                    edges[right_branch]["origin"] = [pixel]
                else:
                    edges[right_branch]["end"] = [pixel]
            edges[right_branch]["pixel_list"][0].append(pixel)
    for branch in edges:
        if len(edges[branch]["origin"]) > 0 and len(edges[branch]["end"]) > 0:
            # TODO(FK): Use pandas.concat instead (Frame.append soon deprecated)
            # graph = graph.append(pd.DataFrame(edges[branch]), ignore_index=True)
            graph = pandas.concat([graph, pd.DataFrame(edges[branch])])
    for index, row in graph.iterrows():
        row["pixel_list"] = order_pixel(row["origin"], row["end"], row["pixel_list"])
    return graph, pixel_branch_dic, is_node, new_index, tip_pixels, tip_branches, neighbour_img

def generate_set_node(graph_tab):
    nodes = set()
    for index, row in graph_tab.iterrows():
        nodes.add(row["origin"])
        nodes.add(row["end"])
    return sorted(nodes)

def order_pixel(pixel_begin, pixel_end, pixel_list):

    ordered_list = [pixel_begin]
    current_pixel = pixel_begin
    precedent_pixel = pixel_begin
    xs = [pixel[0] for pixel in pixel_list]
    ys = [pixel[1] for pixel in pixel_list]

    while current_pixel != pixel_end:
        neighbours = get_neighbours2(current_pixel, np.array(xs), np.array(ys))
        neighbours.discard(precedent_pixel)
        precedent_pixel = current_pixel
        current_pixel = neighbours.pop()
        ordered_list.append(current_pixel)
    return ordered_list

def generate_nx_graph(graph_tab, labeled=False):
    G = nx.Graph()
    pos = {}
    if not labeled:
        nodes = generate_set_node(graph_tab)
    for index, row in graph_tab.iterrows():
        if labeled:
            identifier1 = row["origin_label"]
            identifier2 = row["end_label"]
            pos[identifier1] = np.array(row["origin_pos"]).astype(np.int32)
            pos[identifier2] = np.array(row["end_pos"]).astype(np.int32)
        else:
            identifier1 = nodes.index(row["origin"])
            identifier2 = nodes.index(row["end"])
            pos[identifier1] = np.array(row["origin"]).astype(np.int32)
            pos[identifier2] = np.array(row["end"]).astype(np.int32)
        info = {"weight": len(row["pixel_list"]), "pixel_list": row["pixel_list"]}
        G.add_edges_from([(identifier1, identifier2, info)])
    return (G, pos)

def draw_branch_ids(doc_skel,skel):
    # Extract branches
    graph, pixel_branch_dic, is_node, new_index, tip_pixels, tip_branches,neighbour_img = from_sparse_to_graph(doc_skel)
    
    # Get image dimensions
    height = skel.shape[1]
    width = skel.shape[0]
    branch_image = np.zeros((width,height), dtype=np.uint16)

    # Assign pixels based on branch IDs
    for pixel, branches in pixel_branch_dic.items():
        x, y = pixel
        if len(branches) == 0:
            branch_id = 0
        else:
            branch_id = list(branches)[0]  # Pick one if multiple
        branch_image[x,y] = branch_id  # Use mapped grayscale intensity

    return branch_image