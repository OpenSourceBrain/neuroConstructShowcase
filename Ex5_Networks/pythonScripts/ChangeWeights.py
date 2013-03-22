# -*- coding: utf-8 -*-
#
#
#   File open Ex5_Networks project & generate network & change synaptic weights
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

from sys import *
from time import *
import random

try:
	from java.io import File
except ImportError:
	print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
	print "See http://www.neuroconstruct.org/docs/python.html for more details"
	quit()

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo
from ucl.physiol.neuroconstruct.neuron import NeuronFileManager
from ucl.physiol.neuroconstruct.nmodleditor.processes import ProcessManager

from ucl.physiol.neuroconstruct.project import ConnSpecificProps
from java.util import ArrayList


projFile = File("../Ex5_Networks.ncx")


###########  Main settings  ###########

simConfig =            "Propagation delayed connection"
simDuration =          100  # ms
simDt =                0.01 # ms
neuroConstructSeed =   1234
simulatorSeed =        1111
simRefPrefix =         "RandomWeights_"
runInBackground =      True

#######################################


# Load neuroConstruct project

print "Loading project from "+ projFile.getCanonicalPath()


pm = ProjectManager()
myProject = pm.loadProject(projFile)

myProject.simulationParameters.setDt(simDt)
index = 0

while File( "%s/simulations/%s%i"%(myProject.getProjectMainDirectory().getCanonicalPath(), simRefPrefix,index)).exists():
    index = index+1

simRef = "%s%i"%(simRefPrefix,index)
myProject.simulationParameters.setReference(simRef)

simConfig = myProject.simConfigInfo.getSimConfig(simConfig)

simConfig.setSimDuration(simDuration)

pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
        print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
        sleep(1)

numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()

print "Number of cells generated: " + str(numGenerated)

firstVolBasedConn = simConfig.getNetConns().get(0)
connList = myProject.generatedNetworkConnections.getSynapticConnections(firstVolBasedConn)

synProps = myProject.volBasedConnsInfo.getSynapseList(firstVolBasedConn).get(0)  # Assume only one synapse type in net conn

print "Number of connections in %s with synapse %s: %i" % (firstVolBasedConn, synProps, connList.size())

for conn in connList:
  nextWeight = random.random()
  if conn.props is None:
    csp = ConnSpecificProps(synProps.getSynapseType())
    conn.props = ArrayList()
    conn.props.add(csp)
    
  conn.props.get(0).weight = nextWeight
  print "Weight of one connection set to: %f"%nextWeight


myNetworkMLFile = File("TestNetwork.nml")

pm.saveNetworkStructureXML(myProject, myNetworkMLFile, 0, 0, simConfig.getName(), "Physiological Units")

print "Network structure saved to file: "+ myNetworkMLFile.getAbsolutePath()


if runInBackground:
    myProject.neuronSettings.setNoConsole()
else:
    myProject.neuronFileManager.setQuitAfterRun(1)

myProject.neuronFileManager.generateTheNeuronFiles(simConfig,
                                                    None,
                                                    NeuronFileManager.RUN_HOC,
                                                    simulatorSeed)

print "Generated NEURON files for: "+simRef

compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())

compileSuccess = compileProcess.compileFileWithNeuron(0,0)

print "Compiled NEURON files for: "+simRef

if compileSuccess:
    pm.doRunNeuron(simConfig)
    print "Set running simulation: "+simRef

quit()

