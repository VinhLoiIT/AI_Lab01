from algorithm import *
import threading

def loadMap(filePath):
    print('Loading Map from', filePath)
    algMap = Map()
    algMap.loadFromFile(filePath)
    return algMap

def run_nongui_algorithm(alg, args):
    algMap = loadMap(args.input)

    print('Starting algorithm...')
    alg.setMap(algMap)
    algThread = threading.Thread(target=alg.run)
    algThread.daemon = True
    algThread.start()
    algThread.join(args.time)
    print('Algorithm finished. Writing to file...')
    alg.exportFile(args.output)
    print('Done')
