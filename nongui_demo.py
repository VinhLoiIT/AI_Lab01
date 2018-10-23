from algorithm import Algorithm
from map import Map
import threading

def loadMap(inputFileName):
    print('Loading map...')
    algMap = Map(None, False)
    algMap.loadFromFile(inputFileName)
    return algMap

def applyingHeuristicFunction(heuristicKey):
    print('Applying heuristic function...')
    if heuristicKey == 'euclidean':
        heuristicFunction = Algorithm.HeuristicFunction['Euclidean Distance']
    else:
        heuristicFunction = Algorithm.HeuristicFunction['Diagonal Distance']
    return heuristicFunction

def writeFile(outputFileName, map, result):
    file = open(outputFileName, 'w')
    print(len(result), file=file)
    if len(result) != 0:
        for x in result:
            print(x, file=file, end=' ')
        print(file=file)
        map.exportFile(file)

    file.close()

def run_nongui_astar(args):
    algMap = loadMap(args.input)
    heuristicFunction = applyingHeuristicFunction(args.heuristic)

    print('Starting algorithm...')
    alg = Algorithm(algMap, heuristicFunction)
    alg.AStarOneShot(1)
    print('Algorithm finished. Writing to file...')
    writeFile(args.output, algMap, alg.solution)
    print('Done')


def run_nongui_ara(args):
    algMap = loadMap(args.input)
    heuristicFunction = applyingHeuristicFunction(args.heuristic)

    print('Start algorithm...')
    alg = Algorithm(algMap, heuristicFunction)
    araThread = threading.Thread(target=Algorithm.ARAStar, args=(alg, args.coeff))
    araThread.daemon = True
    araThread.start()
    araThread.join(args.time)
    print('Algorithm finished. Writing to file...')
    writeFile(args.output, algMap, alg.solution)
    print('Finished')