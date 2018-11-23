import csv
from pathlib import Path
from corn import finder as cf
from argparse import ArgumentParser


def write_file(lines, fname):
    with Path(fname).open(mode="w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["x1", "y1", "x2", "y2"])
        for line in lines:
            line = line[0]
            writer.writerow(line)


def main(fname, **kwargs):
    # main CLI entry point
    estimated_corn_rows = cf.find_in_image(
        fname,
        output=kwargs.get("output_image")
    )
    output_fname = kwargs.get("output_lines", None)
    if output_fname:
        write_file(estimated_corn_rows, output_fname)


if __name__ == "__main__":
    # Parse the CLI arguments and pass to the main entry point
    parser = ArgumentParser("An example CLI using the corn library")
    parser.add_argument("fname", type=str, help="path to the image of corn")
    parser.add_argument(
        "--output-image",
        dest="output_image",
        action="store_true",
        help="save a figure showing the final hough lines on "
             "the original image"
    )
    parser.add_argument(
        "--output-lines",
        dest="output_lines",
        type=str,
        help="save a figure showing the final hough lines on "
             "the original image"
    )
    args = parser.parse_args()
    main(**vars(args))
