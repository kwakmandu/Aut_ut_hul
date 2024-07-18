import sys

from shell.shell import Shell


def main():
    try:
        shell = Shell()
        args = sys.argv[1:]  # Get command-line arguments excluding the script name

        if len(args) == 0:
            shell.run()
        elif len(args) == 1:
            shell.run_test_list(args[0])
        else:
            raise ValueError("This script accepts at most one argument.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
