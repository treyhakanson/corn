import numpy as np


def slope(x1, y1, x2, y2):
    # Compute the slope of a line, handling undefined slopes
    if x2 - x1 == 0:
        return float('-inf')
    m = (y2 - y1) / (x2 - x1)
    return m


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
    if (
        q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
        q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])
    ):
        return True
    return False


def orientation(p, q, r):
    val = ((q[1] - p[1]) * (r[0] - q[0]) -
           (q[0] - p[0]) * (r[1] - q[1]))
    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1   # clockwise
    else:
        return 2  # counter-clockwise


def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2 and o3 != o4):
        return True

    # Special Cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if (o1 == 0 and on_segment(p1, p2, q1)):
        return True

    # p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if (o2 == 0 and on_segment(p1, q2, q1)):
        return True

    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if (o3 == 0 and on_segment(p2, p1, q2)):
        return True

    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if (o4 == 0 and on_segment(p2, q1, q2)):
        return True

    return False  # Doesn't fall in any of the above cases
