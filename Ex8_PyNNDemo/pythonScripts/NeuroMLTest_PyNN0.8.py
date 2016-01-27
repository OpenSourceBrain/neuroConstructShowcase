"""
Simple network for testing export to NeuroML v1 & v2

"""
import logging
logging.basicConfig(format='%(levelname)s - %(name)s: %(message)s', level=logging.DEBUG)

import sys
import os

from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]  
exec("from pyNN.%s import *" % simulator_name)

tstop = 500.0

setup(timestep=0.01)
    
cell_params1 = {'tau_refrac':10,'v_thresh':-52.0, 'v_reset':-62.0, 'i_offset': 0.9, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_curr_alpha = Population(1, IF_curr_alpha, cell_params1, label="pop_IF_curr_alpha")
pop_IF_curr_alpha.record('v')
#pop_IF_curr_alpha.initialize('v', -67)

cell_params2 = {'tau_refrac':8,'v_thresh':-50.0, 'v_reset':-70.0, 'i_offset': 1, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_curr_exp = Population(1, IF_curr_exp, cell_params2, label="pop_IF_curr_exp")
pop_IF_curr_exp.record('v')
#pop_IF_curr_exp.initialize('v', -68)

cell_params3 = {'tau_refrac':5,'v_thresh':-50.0, 'v_reset':-65.0, 'i_offset': 0.9, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_cond_alpha = Population(1, IF_cond_alpha, cell_params3, label="pop_IF_cond_alpha")
pop_IF_cond_alpha.record('v')
#pop_IF_cond_alpha.initialize('v', -69)

cell_params4 = {'tau_refrac':5,'v_thresh':-52.0, 'v_reset':-68.0, 'i_offset': 1, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_cond_exp = Population(1, IF_cond_exp, cell_params4, label="pop_IF_cond_exp")
pop_IF_cond_exp.record('v')
#pop_IF_cond_exp.initialize('v', -70)

##TODO: Test a>0!!
cell_params5 = {'tau_refrac':0,'v_thresh':-52.0, 'v_reset':-68.0, 'i_offset': 0.6, 'v_spike': -40, 'a': 0.0, 'b':0.0805}
pop_EIF_cond_exp_isfa_ista = Population(1, EIF_cond_exp_isfa_ista, cell_params5, label="pop_EIF_cond_exp_isfa_ista")
pop_EIF_cond_exp_isfa_ista.record('v')


cell_params6 = {'i_offset': 0.2, 'gbar_K':6.0, 'gbar_Na':20.0}
pop_HH_cond_exp = Population(1, HH_cond_exp, cell_params6, label="pop_HH_cond_exp")
pop_HH_cond_exp.record('v')

# Post synaptic cells
cell_params_post1 = {'tau_refrac':10,'v_thresh':-52.0, 'v_reset':-62.0, 'i_offset': 0}
pop_post1 = Population(1, IF_cond_exp, cell_params_post1, label="pop_post1")
pop_post1.record('v')
cell_params_post2 = {'tau_refrac':10,'v_thresh':-52.0, 'v_reset':-62.0, 'i_offset': 0}
pop_post2 = Population(1, IF_cond_exp, cell_params_post2, label="pop_post2")
pop_post2.record('v')

connE = connect(pop_EIF_cond_exp_isfa_ista, pop_post1, weight=0.006, receptor_type='excitatory',delay=5)
connE = connect(pop_EIF_cond_exp_isfa_ista, pop_post2, weight=0.003, receptor_type='excitatory',delay=10)

run(tstop)

from neo.io import NeoHdf5IO
results_file = "Results/NeuroMLTest_%s.h5" % simulator_name
if os.path.exists(results_file):
    os.remove(results_file)
io = NeoHdf5IO(results_file)


pop_IF_curr_alpha.write_data(io)
pop_IF_curr_exp.write_data(io)
pop_IF_cond_alpha.write_data(io)
pop_IF_cond_exp.write_data(io)
pop_EIF_cond_exp_isfa_ista.write_data(io)
pop_HH_cond_exp.write_data(io)
pop_post1.write_data(io)
pop_post2.write_data(io)


end()

if not '-nogui' in sys.argv:
    if simulator_name in ['neuron', 'nest', 'brian']:
        import matplotlib.pyplot as plt
        
        print("Plotting results of simulation in %s"%simulator_name)

        plt.figure(1)
        for pop in [pop_IF_curr_alpha, pop_IF_curr_exp, pop_IF_cond_exp, pop_IF_cond_alpha]:
            data = pop.get_data()
            vm = data.segments[0].analogsignalarrays[0]
            plt.plot(vm, '-', label=pop.label)
            
        plt.legend()
        
        plt.figure(2)
        for pop in [pop_EIF_cond_exp_isfa_ista, pop_HH_cond_exp]:
            data = pop.get_data()
            vm = data.segments[0].analogsignalarrays[0]
            plt.plot(vm, '-', label=pop.label)
            
        plt.legend()

        plt.figure(3)
        for pop in [pop_post1, pop_post2]:
            data = pop.get_data()
            vm = data.segments[0].analogsignalarrays[0]
            plt.plot(vm, '-', label=pop.label)
            
        plt.legend()


        plt.show()



