from corn import finder as cf
from argparse import ArgumentParser


def main(fname):
    # main CLI entry point
    estimated_corn_rows = cf.find_in_image(fname)


if __name__ == "__main__":
    # Parse the CLI arguments and pass to the main entry point
    parser = ArgumentParser("An example CLI using the corn library")
    parser.add_argument("fname", type=str, help="path to the image of corn")
    args = parser.parse_args()
    main(args.fname)
