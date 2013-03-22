#
#
#   File to test current configuration of HH project.
#
#   To execute this type of file, type '..\..\..\nC.bat -python XXX.py' (Windows)
#   or '../../../nC.sh -python XXX.py' (Linux/Mac). Note: you may have to update the
#   NC_HOME and NC_MAX_MEMORY variables in nC.bat/nC.sh
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

import sys
import os

try:
    from java.io import File
except ImportError:
    print "Note: this file should be run using nC.bat -python XXX.py' or 'nC.sh -python XXX.py'"
    print "See http://www.neuroconstruct.org/docs/python.html for more details"
    quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc

projFile = File(os.getcwd(), "../Ex10_NeuroML2.ncx")

print "Project file for this test: "+ projFile.getAbsolutePath()


##############  Main settings  ##################

simConfigs = []

simConfigs.append("AbstractCells")

simDt =                 0.0001

#simulators =            ["NEURON"]
simulators =            ["NEURON", "LEMS"]


numConcurrentSims =     4

varTimestepNeuron =     False

plotSims =              True
plotVoltageOnly =       True
analyseSims =           True
runInBackground =       True
verbose =               True
runSims =               True

#############################################


def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      numConcurrentSims,
                                      verbose)

    simManager.runMultipleSims(simConfigs =      simConfigs,
                               simDt =           simDt,
                               simulators =      simulators,
                               runInBackground = runInBackground,
                               runSims = runSims,
                               varTimestepNeuron = varTimestepNeuron)
    

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)

    # These were discovered using analyseSims = True above.
    # They need to hold for all simulators
    spikeTimesToCheck = {'CGAbst_0'  : [17.9716, 22.4136, 27.1705, 32.3506, 38.134, 44.8546, 53.2245, 64.6112, 75.5588, 86.8877, 97.8855],
                         'CGAbst2_0'  : [24.3711, 25.5105, 26.722, 28.018, 29.415, 30.9363, 32.6154, 34.506, 36.7044, 39.4271, 43.6248, 77.6337, 79.3465, 81.2841, 83.5555, 86.423, 91.5845, 125.478, 127.191, 129.128, 131.4, 134.267, 139.428, 173.322, 175.035, 176.972, 179.244, 182.111, 187.273],
                         'CGIaF_0'   : [27.3298, 55.0556, 82.7814, 104.1956, 118.0584, 131.9214, 145.7844, 159.6474, 173.5104, 187.3734],
                         'CGIaFRef_0'   : [40.9952, 92.5842, 144.173, 195.762]}

    spikeTimeAccuracy = 0.52

    threshold = {'CGAbst_0'    : -41,
                 'CGAbst2_0'   : 0,
                 'CGIaF_0'     : -55.1,
                 'CGIaFRef_0'  : -55.1}

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy,
                                  threshold = threshold)

    print report

    return report


if __name__ == "__main__":
    testAll()
