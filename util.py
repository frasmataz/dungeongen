import math
import random
import sys
from pprint import pprint

def rectCollide(x1, y1, w1, h1, x2, y2, w2, h2):
    x1 = x1 - 1
    y1 = y1 - 1
    w1 = w1 + 1
    h1 = h1 + 1
    x2 = x2 - 1
    y2 = y2 - 1
    w2 = w2 + 1
    h2 = h2 + 1
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            h1 + y1 > y2)

def interpolate_pixels_along_line(x0, y0, x1, y1):
    """Uses Xiaolin Wu's line algorithm to interpolate all of the pixels along a
    straight line, given two points (x0, y0) and (x1, y1)

    Wikipedia article containing pseudo code that function was based off of:
        http://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm
    """
    pixels = []
    steep = abs(y1 - y0) > abs(x1 - x0)

    # Ensure that the path to be interpolated is shallow and from left to right
    if steep:
        t = x0
        x0 = y0
        y0 = t

        t = x1
        x1 = y1
        y1 = t

    if x0 > x1:
        t = x0
        x0 = x1
        x1 = t

        t = y0
        y0 = y1
        y1 = t

    dx = x1 - x0
    dy = y1 - y0
    if dx != 0 or dy != 0:
        gradient = dy / dx  # slope

        # Get the first given coordinate and add it to the return list
        x_end = round(x0)
        y_end = y0 + (gradient * (x_end - x0))
        xpxl0 = x_end
        ypxl0 = round(y_end)
        if steep:
            pixels.extend([(ypxl0, xpxl0), (ypxl0 + 1, xpxl0)])
        else:
            pixels.extend([(xpxl0, ypxl0), (xpxl0, ypxl0 + 1)])

        interpolated_y = y_end + gradient

        # Get the second given coordinate to give the main loop a range
        x_end = round(x1)
        y_end = y1 + (gradient * (x_end - x1))
        xpxl1 = x_end
        ypxl1 = round(y_end)

        # Loop between the first x coordinate and the second x coordinate, interpolating the y coordinates
        for x in range(xpxl0 + 1, xpxl1):
            if steep:
                pixels.extend([(math.floor(interpolated_y), x), (math.floor(interpolated_y) + 1, x)])

            else:
                pixels.extend([(x, math.floor(interpolated_y)), (x, math.floor(interpolated_y) + 1)])

            interpolated_y += gradient

        # Add the second given coordinate to the given list
        if steep:
            pixels.extend([(ypxl1, xpxl1), (ypxl1 + 1, xpxl1)])
        else:
            pixels.extend([(xpxl1, ypxl1), (xpxl1, ypxl1 + 1)])
    else:
        pixels.extend([(x0, x1), (y0, y1)])

    return pixels

def calculate_distance(p1, p2):
    #Calculate distance between points p1 and p2
    #p1 and p2 are expected to have format [x, y]
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))

def minimum_tree(points):
    #Creates a minimum-spanning tree from a set of points, based on Prim's algorithm.
    out_of_tree = points
    in_tree = []
    edges = []

    first_point = random.choice(out_of_tree)
    in_tree.append(first_point)
    out_of_tree.remove(first_point)

    while len(out_of_tree) > 0:
        shortest_edge = sys.maxsize
        shortest_edge_point_in_tree = None
        shortest_edge_point_out_of_tree = None
        for i in in_tree:
            for o in out_of_tree:
                d = calculate_distance(i, o)
                if d < shortest_edge:
                    shortest_edge = d
                    shortest_edge_point_in_tree = i
                    shortest_edge_point_out_of_tree = o

        in_tree.append(shortest_edge_point_out_of_tree)
        out_of_tree.remove(shortest_edge_point_out_of_tree)
        edges.append([shortest_edge_point_in_tree, shortest_edge_point_out_of_tree])

    return edges