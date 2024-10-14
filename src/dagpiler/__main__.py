# src/dagpiler/__main__.py
import argparse
import sys

from .core import compile_dag
from .dag.printer import print_dag
from .dag.plot_dag import plot_dag
from .init import init

def main():
    # Initialize the top-level parser
    parser = argparse.ArgumentParser(prog="dagpiler", description="Compile a DAG from packaged config files.")
    subparsers = parser.add_subparsers(dest="command")
    
    # Subparser for the 'compile' command
    parser_compile = subparsers.add_parser("compile", help="Compile the specified package, returning a DAG as a NetworkX MultiDiGraph.")
    parser_compile.add_argument("package_name", type=str, help="The name of the package to compile")
    
    # Subparser for the 'plot' command
    parser_plot = subparsers.add_parser("plot", help="Compile and plot the DAG to the specified path.")
    parser_plot.add_argument("output_path", type=str, help="The path where the plot should be saved")

    # Initialize the subparser for the 'init' command
    parser_init = subparsers.add_parser("init", help="Initialize a new package in the current directory.")
    parser_init.add_argument("package_name", type=str, help="The name of the package to initialize")
    
    # Parse arguments
    args = parser.parse_args()
    print(args)

    dag = compile_dag(args.package_name)
    
    # Handle each command
    if args.command == "init":
        return
    elif args.command == "compile":
        return dag
    elif args.command == "plot":
        plot_dag(dag, args.output_path)
    elif args.command == "print":
        print_dag(dag)
    else:
        # If no command is provided, show the help
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":    
    main()       