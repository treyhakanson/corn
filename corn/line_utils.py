import numpy as np


def slope(x1, y1, x2, y2):
    # Compute the slope of a line, handling undefined slopes
    if x2 - x1 == 0:
        return float('-inf')
    m = (y2 - y1) / (x2 - x1)
    return m


def dist(p, q):
    x1, y1 = p
    x2, y2 = q
    d = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
    return d


def ang_dist(m1, m2):
    theta1 = np.arctan(m1)
    theta2 = np.arctan(m2)
    abs_diff = abs(theta1 - theta2)
    d = min(np.pi - abs_diff, abs_diff)
    return d


def scale_line(x1, y1, x2, y2, l):
    # Find the unit length of the line, and scale up to ensure it spans the
    # entire image
    unit_l = np.sqrt(np.square(x1 - x2) + np.square(y1 - y2))
    x3 = x2 + (x2 - x1) / unit_l * l
    y3 = y2 + (y2 - y1) / unit_l * l
    return (int(np.round(x3)), int(np.round(y3)))


def on_segment(p, q, r):
    x1, y1 = p
    x2, y2 = q
    x3, y3 = r

    return (
        x2 <= max(x1, x3) and x2 >= min(x1, x3) and
        y2 <= max(y1, y3) and y2 >= min(y1, y3)
    )


def orientation(p, q, r):
    x1, y1 = p
    x2, y2 = q
    x3, y3 = r
    val = ((y2 - y1) * (x3 - x2) -
           (x2 - x1) * (y3 - y2))

    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1   # clockwise
    else:
        return 2  # counter-clockwise


def has_intersection(p1, q1, p2, q2):
    # Compute orientations
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    interset = False

    # Base case
    interset = interset or (o1 != o2 and o3 != o4)

    # Special Cases
    interset = interset or (o1 == 0 and on_segment(p1, p2, q1))
    interset = interset or (o2 == 0 and on_segment(p1, q2, q1))
    interset = interset or (o3 == 0 and on_segment(p2, p1, q2))
    interset = interset or (o4 == 0 and on_segment(p2, q1, q2))

    return interset
