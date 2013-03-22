#
#
#   File to generate network for execution on parallel NEURON
#   Note this script has only been tested with UCL's cluster!
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
import time


try:
    from java.io import File
except ImportError:
    print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
    print "See http://www.neuroconstruct.org/docs/python.html for more details"
    quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings
from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo

import ncutils as nc # Many useful functions such as SimManager.runMultipleSims found here

projFile = File("../LemsTest.ncx")


###########  Main settings  ###########
simDuration =           500 # ms
simDt =                 0.05 # ms
neuroConstructSeed =    -6831683
simulatorSeed =         11113
simulators =            ["NEURON", "LEMS"]
simulators =            ["NEURON"]
simConfigName =         "AbstNet"

numExcCells = 12
numINCells = 12
defaultSynapticDelay =  0.5

mpiConfigs =              [MpiSettings.MATLEM_1PROC, MpiSettings.MATLEM_2PROC, MpiSettings.MATLEM_4PROC, \
                           MpiSettings.MATLEM_8PROC, MpiSettings.MATLEM_16PROC, MpiSettings.MATLEM_32PROC, \
                           MpiSettings.MATLEM_64PROC]#, MpiSettings.MATLEM_128PROC, MpiSettings.MATLEM_200PROC]
mpiConfigs =              [MpiSettings.LOCAL_SERIAL]
#mpiConfigs =              [MpiSettings.LOCAL_4PROC]
#mpiConfigs =              [MpiSettings.MATLEM_4PROC]
#mpiConfigs =              [MpiSettings.MATLEM_1PROC]

suggestedRemoteRunTime = 2   # mins

varTimestepNeuron =     False

analyseSims =           False
plotSims =              True
plotVoltageOnly =       True

simAllPrefix =          "Py_%i_%i_"%(numExcCells, numINCells)   # Adds a prefix to simulation reference

runInBackground =       mpiConfigs == [MpiSettings.LOCAL_SERIAL]

verbose =               True
runSims =               False
runSims =               True

numConcurrentSims = 4
if mpiConfigs != [MpiSettings.LOCAL_SERIAL]: numConcurrentSims = 30

#######################################


def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      numConcurrentSims = numConcurrentSims,
                                      verbose = verbose)

    ### Change num in each cell group

    simManager.project.cellGroupsInfo.getCellPackingAdapter("ExcCells").setMaxNumberCells(numExcCells)
    simManager.project.cellGroupsInfo.getCellPackingAdapter("INCells").setMaxNumberCells(numINCells)

    ### Change weights in synapses/gap junctions

    simConfig = simManager.project.simConfigInfo.getSimConfig(simConfigName)

    for netConnName in simConfig.getNetConns():
        print "Changing synaptic delay in %s to %f"%(netConnName, defaultSynapticDelay)
        delayGen = NumberGenerator(defaultSynapticDelay)
        for synProps in simManager.project.morphNetworkConnectionsInfo.getSynapseList(netConnName):
            synProps.setDelayGenerator(delayGen)

    # defaultSynapticDelay will be recorded in simulation.props and listed in SimulationBrowser GUI
    SimulationsInfo.addExtraSimProperty("defaultSynapticDelay", str(defaultSynapticDelay))



    allSims = simManager.runMultipleSims(simConfigs =     [simConfigName],
                               simDt =                   simDt,
                               simDuration =             simDuration,
                               simulators =              simulators,
                               runInBackground =         runInBackground,
                               varTimestepNeuron =       varTimestepNeuron,
                               mpiConfigs =              mpiConfigs,
                               suggestedRemoteRunTime =  suggestedRemoteRunTime,
                               simRefGlobalPrefix =      simAllPrefix,
                               runSims =                 runSims,
                               neuroConstructSeed =      neuroConstructSeed,
                               simulatorSeed =           simulatorSeed)

    while (len(simManager.allRunningSims)>0):
        print "Waiting for the following sims to finish: "+str(simManager.allRunningSims)
        time.sleep(5) # wait a while...
        simManager.updateSimsRunning()

    for sim in allSims:
        simDir = File(projFile.getParentFile(), "/simulations/"+sim)

        try:
            simData = SimulationData(simDir)
            simData.initialise()
            simTime = simData.getSimulationProperties().getProperty("RealSimulationTime")
            print "Simulation: %s took %s seconds"%(sim, simTime)

        except:
            print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()

    if mpiConfigs == [MpiSettings.LOCAL_SERIAL] or mpiConfigs == [MpiSettings.MATLEM_1PROC]:
        simManager.reloadSims(plotVoltageOnly =   True,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)

if __name__ == "__main__":
    testAll()