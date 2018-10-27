import argparse
from gui_demo import run_app
from nongui_demo import run_nongui_algorithm
from algorithm import AStarAlgorithm, ARAAlgorithm, HeuristicFunctions
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="LAB01 Project: Finding path by using AStar or ARA algorithm")

    subparsers = parser.add_subparsers(help='Supported commands', dest='command')

    gui_parser = subparsers.add_parser('gui')
    gui_parser.set_defaults()

    astar_parser = subparsers.add_parser('astar')
    astar_parser.add_argument('-i', '--input', help='Path to input file', type=str, required=True)
    astar_parser.add_argument('-o', '--output', help='Path to output file', type=str, required=True)
    astar_parser.add_argument('-hf', '--heuristic',
                              help='Heuristic function',
                              type=str,
                              choices=['euclidean', 'diagonal'],
                              default='euclidean')
    astar_parser.set_defaults(time=None)

    ara_parser = subparsers.add_parser('ara')
    ara_parser.add_argument('-i', '--input', help='Path to input file', type=str)
    ara_parser.add_argument('-o', '--output', help='Path to output file', type=str)
    ara_parser.add_argument('-hf', '--heuristic',
                              help='Heuristic function',
                              type=str,
                              choices=['euclidean', 'diagonal'],
                              default='euclidean')
    ara_parser.add_argument('-t', '--time', help='Time limitation (in milliseconds)', type=float, default=50)
    ara_parser.set_defaults()

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        if args.command == 'gui':
            run_app()
        else:
            if args.heuristic == 'euclidean':
                heuristicFunction = HeuristicFunctions['Euclidean Distance']
            else:
                heuristicFunction = HeuristicFunctions['Diagonal Distance']

            if args.command == 'ara':
                alg = ARAAlgorithm(heuristicFunction)
            else:
                alg = AStarAlgorithm(heuristicFunction)
            run_nongui_algorithm(alg, args)
