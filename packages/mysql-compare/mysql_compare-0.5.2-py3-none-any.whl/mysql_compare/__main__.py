import argparse

from . import mysql_compare_forward, mysql_compare_reverse


def main():
    parser = argparse.ArgumentParser(description="x.py script")
    parser.add_argument("--direction", choices=["forward", "reverse"], required=True, help="Choose which script to execute (a or b)")

    args, unknown_args = parser.parse_known_args()

    if args.direction == "forward":
        mysql_compare_forward.run(unknown_args)
    elif args.direction == "reverse":
        mysql_compare_reverse.run(unknown_args)


if __name__ == "__main__":
    main()
