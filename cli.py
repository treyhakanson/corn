from corn import finder as cf
from argparse import ArgumentParser


def main(fname, **kwargs):
    # main CLI entry point
    cf.find_in_image(fname, **kwargs)


if __name__ == "__main__":
    # Parse the CLI arguments and pass to the main entry point
    parser = ArgumentParser("An example CLI using the corn library")
    parser.add_argument("fname", type=str, help="path to the image of corn")
    parser.add_argument("--output", dest="output", action="store_true",
                        help="save a figure showing the final hough lines on "
                             "the original image")
    args = parser.parse_args()
    main(**vars(args))
