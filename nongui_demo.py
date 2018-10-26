from algorithm import *
from map import Map
import threading

def loadMap(inputFileName):
    print('Loading map...')
    algMap = Map()
    algMap.loadFromFile(inputFileName)
    return algMap

def applyingHeuristicFunction(heuristicKey):
    print('Applying heuristic function...')
    if heuristicKey == 'euclidean':
        heuristicFunction = HeuristicFunctions['Euclidean Distance']
    else:
        heuristicFunction = HeuristicFunctions['Diagonal Distance']
    return heuristicFunction

def writeFile(outputFileName, map, result):
    file = open(outputFileName, 'w')
    print(len(result), file=file)
    if len(result) != 0:
        for x in result:
            print('({0}, {1})'.format(x.row, x.col), end=' ', file=file)
        print(file=file)
        map.exportFile(file)

    file.close()

def run_nongui_astar(args):
    algMap = loadMap(args.input)
    heuristicFunction = applyingHeuristicFunction(args.heuristic)

    print('Starting algorithm...')
    alg = AStarAlgorithm(algMap, heuristicFunction)
    alg.run()
    print('Algorithm finished. Writing to file...')
    writeFile(args.output, algMap, alg.solution)
    print('Done')


def run_nongui_ara(args):
    algMap = loadMap(args.input)
    heuristicFunction = applyingHeuristicFunction(args.heuristic)

    alg = ARAAlgorithm(algMap, heuristicFunction)
    alg.setCoeff(args.coeff)

    print('Start algorithm...')
    araThread = threading.Thread(target=alg.run)
    araThread.daemon = True
    araThread.start()
    araThread.join(args.time)
    print('Algorithm finished. Writing to file...')
    writeFile(args.output, algMap, alg.solution)
    print('Finished')
