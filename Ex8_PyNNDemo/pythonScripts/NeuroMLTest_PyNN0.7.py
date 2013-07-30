"""
Simple network for testing export to NeuroML v1 & v2

"""
import logging
logging.basicConfig(format='%(levelname)s - %(name)s: %(message)s', level=logging.DEBUG)


from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]  
exec("from pyNN.%s import *" % simulator_name)

tstop = 500.0

setup(timestep=0.01)
    
cell_params1 = {'tau_refrac':10,'v_thresh':-52.0, 'v_reset':-62.0, 'i_offset': 0.9, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_curr_alpha = Population(1, IF_curr_alpha, cell_params1, label="pop_IF_curr_alpha")
pop_IF_curr_alpha.record_v()
#pop_IF_curr_alpha.initialize('v', -67)

cell_params2 = {'tau_refrac':8,'v_thresh':-50.0, 'v_reset':-70.0, 'i_offset': 1, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_curr_exp = Population(1, IF_curr_exp, cell_params2, label="pop_IF_curr_exp")
pop_IF_curr_exp.record_v()
#pop_IF_curr_exp.initialize('v', -68)

cell_params3 = {'tau_refrac':5,'v_thresh':-50.0, 'v_reset':-65.0, 'i_offset': 0.9, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_cond_alpha = Population(1, IF_cond_alpha, cell_params3, label="pop_IF_cond_alpha")
pop_IF_cond_alpha.record_v()
#pop_IF_cond_alpha.initialize('v', -69)

cell_params4 = {'tau_refrac':5,'v_thresh':-52.0, 'v_reset':-68.0, 'i_offset': 1, 'tau_syn_E'  : 2.0, 'tau_syn_I': 5.0}
pop_IF_cond_exp = Population(1, IF_cond_exp, cell_params4, label="pop_IF_cond_exp")
pop_IF_cond_exp.record_v()
#pop_IF_cond_exp.initialize('v', -70)

##TODO: Test a>0!!
cell_params5 = {'tau_refrac':0,'v_thresh':-52.0, 'v_reset':-68.0, 'i_offset': 0.6, 'v_spike': -40, 'a': 0.0, 'b':0.0805}
pop_EIF_cond_exp_isfa_ista = Population(1, EIF_cond_exp_isfa_ista, cell_params5, label="pop_EIF_cond_exp_isfa_ista")
pop_EIF_cond_exp_isfa_ista.record_v()


cell_params6 = {'i_offset': 0.2, 'gbar_K':6.0, 'gbar_Na':20.0}
pop_HH_cond_exp = Population(1, HH_cond_exp, cell_params6, label="pop_HH_cond_exp")
pop_HH_cond_exp.record_v()

# Post synaptic cells
cell_params_post1 = {'tau_refrac':10,'v_thresh':-52.0, 'v_reset':-62.0, 'i_offset': 0}
pop_post1 = Population(1, IF_cond_exp, cell_params_post1, label="pop_post1")
pop_post1.record_v()
cell_params_post2 = {'tau_refrac':10,'v_thresh':-52.0, 'v_reset':-62.0, 'i_offset': 0}
pop_post2 = Population(1, IF_cond_exp, cell_params_post2, label="pop_post2")
pop_post2.record_v()

connE = connect(pop_EIF_cond_exp_isfa_ista, pop_post1, weight=0.006, synapse_type='excitatory',delay=5)
connE = connect(pop_EIF_cond_exp_isfa_ista, pop_post2, weight=0.003, synapse_type='excitatory',delay=10)

run(tstop)

pop_IF_curr_alpha.print_v("Results/NeuroMLTest_curr_alpha_%s.v" % simulator_name)
pop_IF_curr_exp.print_v("Results/NeuroMLTest_curr_exp_%s.v" % simulator_name)
pop_IF_cond_alpha.print_v("Results/NeuroMLTest_cond_alpha_%s.v" % simulator_name)
pop_IF_cond_exp.print_v("Results/NeuroMLTest_cond_exp_%s.v" % simulator_name)
pop_EIF_cond_exp_isfa_ista.print_v("Results/NeuroMLTest_eif_exp_%s.v" % simulator_name)
pop_HH_cond_exp.print_v("Results/NeuroMLTest_hh_exp_%s.v" % simulator_name)

pop_post1.print_v("Results/NeuroMLTest_post_%s.v" % simulator_name)
pop_post2.print_v("Results/NeuroMLTest_post_%s.v" % simulator_name)

end()

if simulator_name in ['neuron', 'nest', 'brian']:
    import matplotlib.pyplot as plt

    plt.figure(1)
    for pop in [pop_IF_curr_alpha, pop_IF_curr_exp, pop_IF_cond_exp, pop_IF_cond_alpha]:
        vm = pop.get_v()
        plt.plot(vm[:,1],vm[:,2], '-')

    plt.figure(2)
    for pop in [pop_EIF_cond_exp_isfa_ista, pop_HH_cond_exp]:
        vm = pop.get_v()
        plt.plot(vm[:,1],vm[:,2], '-')

    plt.figure(3)
    for pop in [pop_post1, pop_post2]:
        vm = pop.get_v()
        plt.plot(vm[:,1],vm[:,2], '-')

    plt.show()



