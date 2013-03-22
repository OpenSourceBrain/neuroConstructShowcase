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

simConfigs.append("Test NeuroML2 ionChannel")

simDt =                 0.0005

#simulators =            ["NEURON"]
simulators =            ["NEURON", "LEMS"]


numConcurrentSims =     4

varTimestepNeuron =     False

plotSims =              True
plotVoltageOnly =       True
analyseSims =           True
runInBackground =       True
verbose =               False

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
                               varTimestepNeuron = varTimestepNeuron)
    

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)

    # These were discovered using analyseSims = True above.
    # They need to hold for all simulators
    spikeTimesToCheck = {'SampleCellGroup_0' : [102.2, 118.4, 134.4, 150.3, 166.3, 182.3, 198.3]}

    spikeTimeAccuracy = 0.1

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy)

    print report

    return report


if __name__ == "__main__":
    testAll()
