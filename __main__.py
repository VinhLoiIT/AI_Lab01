import argparse
from gui_demo import run_app
from nongui_demo import run_nongui_ara, run_nongui_astar


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""
        LAB01 Project: Finding path by using AStar or ARA algorithm
        Student ID = 1612348
        Student ID = 1612756
    """)

    subparsers = parser.add_subparsers(help='Algorithms', dest='command')

    gui_parser = subparsers.add_parser('gui')
    gui_parser.set_defaults(func=run_app)

    astar_parser = subparsers.add_parser('astar')
    astar_parser.add_argument('-i', '--input', help='Path to input file', type=str, required=True)
    astar_parser.add_argument('-o', '--output', help='Path to output file', type=str, required=True)
    astar_parser.add_argument('-hf', '--heuristic',
                              help='Heuristic function',
                              type=str,
                              choices=['euclidean', 'diagonal'],
                              default='euclidean')
    astar_parser.set_defaults(func=run_nongui_astar)

    ara_parser = subparsers.add_parser('ara')
    ara_parser.add_argument('-i', '--input', help='Path to input file', type=str)
    ara_parser.add_argument('-o', '--output', help='Path to output file', type=str)
    ara_parser.add_argument('-c', '--coeff', help='Coefficient of heuristic function', type=float, default=3)
    ara_parser.add_argument('-hf', '--heuristic',
                              help='Heuristic function',
                              type=str,
                              choices=['euclidean', 'diagonal'],
                              default='euclidean')
    ara_parser.add_argument('-t', '--time', help='Time limitation (in second)', type=float, default=3)
    ara_parser.set_defaults(func=run_nongui_ara)

    args = parser.parse_args()

    if args.command == 'gui':
        run_app()
    elif args.command == 'astar':
        run_nongui_astar(args)
    elif args.command == 'ara':
        run_nongui_ara(args)
