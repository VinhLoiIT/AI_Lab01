import argparse
from algorithm import Algorithm, AlgorithmState
from map import Map
from gui_demo import run_app
import threading
import time

def writeFile(outputFileName, map, result):
    file = open(outputFileName, 'w')
    print(len(result), file=file)
    if len(result) != 0:
        for x in result:
            print(x, file=file, end=' ')
        print(file=file)
        map.exportFile(file)

    file.close()

def run_gui(args):
    run_app()

def run_nongui_astar(args):
    algMap = Map(None)
    algMap.loadFromFile(args.input)
    if args.heuristic == 'euclidean':
        heuristicFunction = Algorithm.HeuristicFunction['Euclidean Distance']
    else:
        heuristicFunction = Algorithm.HeuristicFunction['Diagonal Distance']

    alg = Algorithm(algMap, heuristicFunction)
    alg.AStarOneShot(1)
    result = alg.solution

    writeFile(args.output, algMap, result)


def run_nongui_ara(args):
    print(args)
    algMap = Map(None)
    algMap.loadFromFile(args.input)
    if args.heuristic == 'euclidean':
        heuristicFunction = Algorithm.HeuristicFunction['Euclidean Distance']
    else:
        heuristicFunction = Algorithm.HeuristicFunction['Diagonal Distance']

    alg = Algorithm(algMap, heuristicFunction)

    # stopFlag = threading.Event()
    araThread = threading.Thread(target=Algorithm.ARAStar, args=(alg, args.coeff))
    araThread.daemon = True
    araThread.start()
    araThread.join(args.time)

    # time.sleep(args.time)
    # stopFlag.set()

    result = alg.solution
    writeFile(args.output, algMap, result)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""
        LAB01 Project: Finding path by using AStar or ARA algorithm
        Student ID = 1612348
        Student ID = 1612756
    """)

    subparsers = parser.add_subparsers(help='Algorithms', dest='command')

    gui_parser = subparsers.add_parser('gui')
    gui_parser.set_defaults(func=run_gui)

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
        run_gui(args)
    elif args.command == 'astar':
        run_nongui_astar(args)
    elif args.command == 'ara':
        run_nongui_ara(args)

#TODO: cach su dung
#vao commandline:
#py __main__.py ara -i test/input_8.txt -o output_8_ara.txt -hf euclidean -t 0.5 -c 3
