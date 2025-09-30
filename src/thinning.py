import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas

def zhang_suen_step(img, step):
    """One iteration of Zhang_suen_thinning"""
    changed = False
    rows, cols = img.shape
    deletion = np.zeros((rows, cols))
    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            if img[y][x]:
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbors(x, y, img)
                if 2 <= sum(n) <= 6 and transitions(n) == 1:
                    if step == 0:
                        if P2 * P4 * P6 == 0 and P4 * P6 * P8 == 0:
                            deletion[y][x] = 1
                    else:
                        if P2 * P4 * P8 == 0 and P2 * P6 * P8 == 0:
                            deletion[y][x] = 1
    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            if deletion[y][x] == 1:
                img[y][x] = 0
                changed = True
    return img, changed


def zhang_suen_thinning(image):
    """Zhang_suen_thinning"""
    # Convert the image to binary
    img = np.where(image > 0, 1, 0)
    changed = True
    while changed:
        img, changed1 = zhang_suen_step(img, 0)
        img, changed2 = zhang_suen_step(img, 1)
        changed = changed1 or changed2
    return img

def neighbors(x, y, img):
    """Return 8-neighbors of image point P1(x, y), in a clockwise order"""
    return (
        img[y - 1][x],
        img[y - 1][x + 1],
        img[y][x + 1],
        img[y + 1][x + 1],
        img[y + 1][x],
        img[y + 1][x - 1],
        img[y][x - 1],
        img[y - 1][x - 1],
    )


def transitions(neighbors):
    """No. of 0,1 patterns (transitions from 0 to 1) in the ordered sequence"""
    n = neighbors
    tot = 0
    for i in range(len(n)):
        tot += (n[i], n[(i + 1) % len(n)]) == (0, 1)
    return tot