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
    print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
    print "See http://www.neuroconstruct.org/docs/python.html for more details"
    quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc

projFile = File(os.getcwd(), "../Ex8_PyNNDemo.ncx")

print "Project file for this test: "+ projFile.getAbsolutePath()


##############  Main settings  ##################

simConfigs = []

simConfigs.append("TestPyNN_NML2")

simDt =                 0.001

simulators =            ["PYNN_NEST", "PYNN_NEURON", "PYNN_BRIAN"]
simulators =            ["PYNN_NEST", "PYNN_NEURON", "LEMS"]
simulators =            ["PYNN_NEURON", "LEMS"]
#simulators =            ["NEURON"]


numConcurrentSims =     4

varTimestepNeuron =     False

plotSims =              True
plotVoltageOnly =       True
analyseSims =           True
runInBackground =       True
verbose =               True

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
                               runInBackground = runInBackground)
    

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)


    # These were discovered using analyseSims = True above.
    # They need to hold for all simulators
    spikeTimesToCheck = {'CG_PyNN_EIFe_0' : [26.77, 82.15, 176.784, 285.342, 394.576], \
                         'CG_PyNN_IFa_0' : [35.342, 78.506, 121.67, 164.834, 207.998, 251.162, 294.326, 337.49, 380.654, 423.818, 466.982], \
                         'CG_PyNN_HH_0' : [11.584, 40.406, 69.272, 98.136, 127.0, 155.864, 184.728, 213.594, 242.458, 271.322, 300.186, 329.052, 357.916, 386.78, 415.644, 444.508, 473.374]}

    spikeTimeAccuracy = 0.81

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy,
                                  threshold = -45.1)

    print report

    return report


if __name__ == "__main__":
    testAll()
