import cv2
import numpy as np
from . import line_utils


def take_rng(data, low, high):
    # Take a range of data from an array
    n = len(data)
    i = int(n * low)
    j = int(n * high)
    return data[i:j]


def show_image(img):
    # Show an image in a scaled window
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_in_image(imgfname):
    # Read in the image, perform some initial formatting and convert to black
    # and white
    img = cv2.imread(imgfname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blrimg = cv2.medianBlur(gray, 11)
    (thresh, bw) = cv2.threshold(
        blrimg,
        128,
        255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )

    # Close the image
    dlimg1 = cv2.dilate(bw, (100, 100), iterations=10)
    eimg = cv2.erode(dlimg1, (100, 100), iterations=10)

    # Perform edge detection, perform dilation to reinforce edges, and then
    # perform a probablistic Hough transform
    edges = cv2.Canny(eimg, 254, 254, apertureSize=3, L2gradient=True)
    dledges = cv2.dilate(edges, (100, 100), iterations=20)
    lines = cv2.HoughLinesP(
        dledges,
        1,
        np.pi/180,
        threshold=30,
        minLineLength=75
    )

    # Compute the slopes of each line, and find the median
    slopes = np.zeros(len(lines))
    for i, line in enumerate(lines):
        slopes[i] = line_utils.slope(*line[0])
    m_med = np.median(slopes)

    # Get the sorted indices of the slopes, and drop the bottom and top 10%
    sorted_idx = take_rng(np.argsort(slopes), 0.10, 0.90)
    lines = lines[sorted_idx]

    # Filter out lines that vary significantly from the median
    # NOTE: this makes the assumption that the rows of corn are approximately
    # parallel
    para_thresh = 3 * np.pi / 180  # 3deg
    j = 0
    idx = np.zeros(len(lines), dtype=int)
    for i, line in enumerate(lines):
        d = line_utils.ang_dist(m_med, line_utils.slope(*line[0]))
        if d < para_thresh:
            idx[j] = i
            j += 1
    lines = lines[np.trim_zeros(idx)]

    # Drop intersecting line segments
    j = 0
    idx = np.zeros(len(lines), dtype=int)
    h, _, _ = img.shape
    for i, line1 in enumerate(lines, 0):
        unique = True
        for line2 in lines[i + 1:]:
            p1 = line_utils.scale_line(*line1[0], h)
            q1 = line_utils.scale_line(*line1[0], -h)
            p2 = line_utils.scale_line(*line2[0], h)
            q2 = line_utils.scale_line(*line2[0], -h)
            if line_utils.do_intersect(p1, q1, p2, q2):
                unique = False
                break
        if unique:
            idx[j] = i
            j += 1
    lines = lines[np.trim_zeros(idx)]

    # Draw the lines on the original image, and show the result
    h, _, _ = img.shape
    for line in lines:
        x3, y3 = line_utils.scale_line(*line[0], h)
        x4, y4 = line_utils.scale_line(*line[0], -h)
        cv2.line(img, (x3, y3), (x4, y4), (0, 0, 255), 2)
    show_image(img)

    # Return the results
    return lines
