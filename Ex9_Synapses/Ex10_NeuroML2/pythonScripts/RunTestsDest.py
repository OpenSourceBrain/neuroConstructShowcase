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

simConfigs.append("Destexhe09Cells")

simDt =                 0.001

#simulators =            ["NEURON"]
simulators =            ["NEURON", "LEMS"]


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
                               runInBackground = runInBackground,
                               varTimestepNeuron = varTimestepNeuron)
    

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)

    # These were discovered using analyseSims = True above.
    # They need to hold for all simulators
    spikeTimesToCheck = {'FS_0'  : [209.779, 219.611, 229.447, 239.287, 249.131, 258.979, 268.831, 278.686, 288.546, 298.41, 308.277, 318.147, 328.022, 337.899, 347.781, 357.665, 367.553, 377.445, 387.339, 397.236, 407.137, 417.041, 426.948, 436.858, 446.771, 456.687, 466.606, 476.528, 486.452, 496.378, 506.308, 516.24, 526.174, 536.112, 546.051, 555.994, 565.938, 575.886, 585.835, 595.79],
                         'RS_04_0' : [209.779, 222.027, 238.189, 261.603, 301.844, 387.788, 518.983], 
                         'RS_005_0' : [209.779, 219.859, 230.202, 240.815, 251.709, 262.893, 274.376, 286.169, 298.281, 310.722, 323.503, 336.63, 350.115, 363.967, 378.194, 392.803, 407.802, 423.198, 438.997, 455.202, 471.816, 488.843, 506.283, 524.135, 542.397, 561.066, 580.135, 599.598]}

    spikeTimeAccuracy = 0.02

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy,
                                  threshold = -50.01)

    print report

    return report


if __name__ == "__main__":
    testAll()
