from z3 import *

from lib.Lib import compute_cycle_period
from window_demo.topo_and_streams_txt_parser_for_window_demo import *



def construct_constraints_for_window_demo(link_obj_set,
                                          stream_obj_set,
                                          stream_instance_obj_set,
                                          sync_precision):
    formula = []
    hyper_period = compute_cycle_period(*[stream_obj.period
                                          for stream_obj in stream_obj_set])
    

    
    for link_obj in link_obj_set:
        gcl_len = link_obj.gcl_len
        stream_id_and_hop_id_set = link_obj.stream_set
        if len(stream_id_and_hop_id_set) != 0:
            phi = link_obj.phi_array[0]
            tau = link_obj.tau_array[gcl_len - 1]
            constraint_1 = And(phi >= 0, tau < hyper_period)
            
            formula.append(constraint_1)
            
    

    for link_obj in link_obj_set:
        gcl_len = link_obj.gcl_len
        stream_id_and_hop_id_set = link_obj.stream_set
        if len(stream_id_and_hop_id_set) != 0:
            for k in range(gcl_len):
                kappa = link_obj.kappa_array[k]
                constraint_1 = And(kappa >= 0, kappa < link_obj.st_queues)
                formula.append(constraint_1)
                
    

    
    for instance_obj_set_per_stream in stream_instance_obj_set:
        for instance_obj_set_per_link in instance_obj_set_per_stream:
            j = 0
            for instance_obj in instance_obj_set_per_link:
                link_id = instance_obj.link_id
                stream_id = instance_obj.stream_id
                period = stream_obj_set[stream_id].period
                phi = link_obj_set[link_id].phi_array
                tau = link_obj_set[link_id].tau_array
                omega = instance_obj.omega
                constraint_2 = And(phi[omega] >= j * period,
                                   tau[omega] < (j + 1) * period)
                formula.append(constraint_2)
                
                j += 1
    

    
    for link_obj in link_obj_set:
        gcl_len = link_obj.gcl_len
        for i in range(gcl_len - 1):
            phi = link_obj.phi_array[i + 1]
            tau = link_obj.tau_array[i]
            constraint_3 = (tau <= phi)
            formula.append(constraint_3)
            
    

    
    for instance_obj_set_per_stream in stream_instance_obj_set:
        for instance_obj_set_per_link in instance_obj_set_per_stream:
            for instance_obj in instance_obj_set_per_link:
                link_id = instance_obj.link_id
                gcl_len = link_obj_set[link_id].gcl_len
                omega = instance_obj.omega
                constraint_4 = And(omega >= 0, omega <= gcl_len - 1)
                formula.append(constraint_4)
                
    

    
    for link_obj in link_obj_set:
        gcl_len = link_obj.gcl_len
        phi_array = link_obj.phi_array
        
        tau_0_array = link_obj.tau_0_array
        if len(link_obj.stream_set) == 0:
            continue
        for k in range(gcl_len):
            
            
            
            
            
            
            constraint_5 = (tau_0_array == Store(tau_0_array, k, phi_array[k]))
            formula.append(constraint_5)
            

    
    for link_obj in link_obj_set:
        gcl_len = link_obj.gcl_len
        tau_1_array = link_obj.tau_1_array
        
        if len(link_obj.stream_set) == 0:
            continue
        for k in range(gcl_len):
            tau_1_array = Store(tau_1_array, k, 0)
            link_obj.tau_1_array = tau_1_array

    
    for stream_instance_obj_set_per_stream in stream_instance_obj_set:
        for stream_instance_obj_set_per_link in stream_instance_obj_set_per_stream:
            for stream_instance_obj in stream_instance_obj_set_per_link:
                link_id = stream_instance_obj.link_id
                tau_1_array = link_obj_set[link_id].tau_1_array
                omega = stream_instance_obj.omega
                stream_id = stream_instance_obj.stream_id
                hop_id = stream_instance_obj.hop_id
                trans_duration = \
                    stream_obj_set[stream_id].route_obj_set[hop_id].trans_duration
                tau_1_array = Store(tau_1_array, omega, tau_1_array[omega] + trans_duration)
                link_obj_set[link_id].tau_1_array = tau_1_array

    
    for link_obj in link_obj_set:
        gcl_len = link_obj.gcl_len
        tau_array = link_obj.tau_array
        tau_0_array = link_obj.tau_0_array
        tau_1_array = link_obj.tau_1_array
        if len(link_obj.stream_set) == 0:
            continue
        for k in range(gcl_len):
            
            constraint_5 = (tau_array == Store(tau_array, k, tau_0_array[k] + tau_1_array[k]))
            formula.append(constraint_5)
            

    
    
    for instance_obj_set_per_stream in stream_instance_obj_set:
        route_path_len = len(instance_obj_set_per_stream)
        instance_num_in_hyper_period = len(instance_obj_set_per_stream[0])
        for j in range(instance_num_in_hyper_period):
            for k in range(route_path_len - 1):
                pre_instance_obj = instance_obj_set_per_stream[k][j]
                suc_instance_obj = instance_obj_set_per_stream[k + 1][j]
                pre_link_id = pre_instance_obj.link_id
                suc_link_id = suc_instance_obj.link_id
                pre_tau = link_obj_set[pre_link_id].tau_array
                suc_phi = link_obj_set[suc_link_id].phi_array
                pre_omega = pre_instance_obj.omega
                suc_omega = suc_instance_obj.omega
                constraint_6 = (pre_tau[pre_omega] + sync_precision <= suc_phi[suc_omega])
                formula.append(constraint_6)
                

    

    
    
    
    
    
    for link_obj in link_obj_set:
        
        
        
        stream_id_and_hop_id_set = link_obj.stream_set
        stream_num = len(stream_id_and_hop_id_set)

        
        ab_tau_array = link_obj.tau_array
        
        ab_phi_array = link_obj.phi_array
        
        ab_kappa_array = link_obj.kappa_array

        
        for i in range(stream_num):
            for j in range(i + 1, stream_num):
                i_stream_id = stream_id_and_hop_id_set[i]['stream_id']
                j_stream_id = stream_id_and_hop_id_set[j]['stream_id']

                i_ab_hop_id = stream_id_and_hop_id_set[i]['hop_id']
                j_ab_hop_id = stream_id_and_hop_id_set[j]['hop_id']

                
                i_stream_instance_obj_set_at_ab_hop = stream_instance_obj_set[i_stream_id][i_ab_hop_id]
                j_stream_instance_obj_set_at_ab_hop = stream_instance_obj_set[j_stream_id][j_ab_hop_id]

                
                
                if i_ab_hop_id == 0 and j_ab_hop_id == 0:
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                            
                    pass

                else:
                    
                    
                    i_xa_hop_id = stream_id_and_hop_id_set[i]['hop_id'] - 1
                    j_ya_hop_id = stream_id_and_hop_id_set[j]['hop_id'] - 1
                    
                    
                    i_xa_link_id = stream_obj_set[i_stream_id].route_obj_set[i_xa_hop_id].link_id
                    j_ya_link_id = stream_obj_set[j_stream_id].route_obj_set[j_ya_hop_id].link_id
                    
                    i_xa_hop_phi_array = link_obj_set[i_xa_link_id].phi_array
                    j_ya_hop_phi_array = link_obj_set[j_ya_link_id].phi_array
                    
                    i_stream_instance_obj_set_at_xa_hop = stream_instance_obj_set[i_stream_id][i_xa_hop_id]
                    j_stream_instance_obj_set_at_ya_hop = stream_instance_obj_set[j_stream_id][j_ya_hop_id]

                    
                    for (k_ab_instance_obj, k_xa_instance_obj) in \
                            zip(i_stream_instance_obj_set_at_ab_hop, i_stream_instance_obj_set_at_xa_hop):
                        for (l_ab_instance_obj, l_ya_instance_obj) in \
                                zip(j_stream_instance_obj_set_at_ab_hop, j_stream_instance_obj_set_at_ya_hop):
                            i_k_ab_omega = k_ab_instance_obj.omega
                            j_l_ab_omega = l_ab_instance_obj.omega
                            i_k_xa_omega = k_xa_instance_obj.omega
                            j_l_ya_omega = l_ya_instance_obj.omega

                            constraint_7 = Or(ab_tau_array[i_k_ab_omega] + sync_precision <=
                                              j_ya_hop_phi_array[j_l_ya_omega],
                                              ab_tau_array[j_l_ab_omega] + sync_precision <=
                                              i_xa_hop_phi_array[i_k_xa_omega],
                                              ab_kappa_array[i_k_ab_omega] != ab_kappa_array[j_l_ab_omega],
                                              i_k_ab_omega == j_l_ab_omega)
                            formula.append(constraint_7)
                            

    
    for instance_obj_set_per_stream in stream_instance_obj_set:
        instance_num_in_hyper_period = len(instance_obj_set_per_stream[0])

        first_link_id = instance_obj_set_per_stream[0][0].link_id
        last_link_id = instance_obj_set_per_stream[-1][0].link_id
        stream_id = instance_obj_set_per_stream[0][0].stream_id
        last_tau_array = link_obj_set[last_link_id].tau_array
        first_phi_array = link_obj_set[first_link_id].phi_array
        latency_requirement = stream_obj_set[stream_id].latency_requirement
        for i in range(instance_num_in_hyper_period):
            first_instance_obj = instance_obj_set_per_stream[0][i]
            last_instance_obj = instance_obj_set_per_stream[-1][i]
            first_omega = first_instance_obj.omega
            last_omega = last_instance_obj.omega
            constraint_8 = (last_tau_array[last_omega] - first_phi_array[first_omega] <=
                            latency_requirement - sync_precision)
            formula.append(constraint_8)
            

    
    
    for instance_obj_set_per_stream in stream_instance_obj_set:
        instance_obj_set_at_first_link = instance_obj_set_per_stream[0]
        instance_num_in_hyper_period = len(instance_obj_set_at_first_link)

        link_id = instance_obj_set_at_first_link[0].link_id
        phi_array = link_obj_set[link_id].phi_array
        tau_array = link_obj_set[link_id].tau_array

        stream_id = instance_obj_set_at_first_link[0].stream_id
        period = stream_obj_set[stream_id].period
        trans_duration = stream_obj_set[stream_id].route_obj_set[0].trans_duration
        jitter_requirement = stream_obj_set[stream_id].jitter_requirement
        for j in range(instance_num_in_hyper_period):
            for k in range(instance_num_in_hyper_period):
                j_omega = instance_obj_set_at_first_link[j].omega
                k_omega = instance_obj_set_at_first_link[k].omega

                constraint_9 = ((tau_array[j_omega] - j * period) - (phi_array[k_omega] - k * period) -
                                trans_duration <= jitter_requirement)
                formula.append(constraint_9)
                

    
    for instance_obj_set_per_stream in stream_instance_obj_set:
        instance_obj_set_at_last_link = instance_obj_set_per_stream[-1]
        instance_num_in_hyper_period = len(instance_obj_set_at_last_link)

        link_id = instance_obj_set_at_last_link[0].link_id
        phi_array = link_obj_set[link_id].phi_array
        tau_array = link_obj_set[link_id].tau_array

        stream_id = instance_obj_set_at_last_link[0].stream_id
        period = stream_obj_set[stream_id].period
        trans_duration = stream_obj_set[stream_id].route_obj_set[0].trans_duration
        jitter_requirement = stream_obj_set[stream_id].jitter_requirement
        for j in range(instance_num_in_hyper_period):
            for k in range(instance_num_in_hyper_period):
                j_omega = instance_obj_set_at_last_link[j].omega
                k_omega = instance_obj_set_at_last_link[k].omega

                constraint_9 = ((tau_array[j_omega] - j * period) - (phi_array[k_omega] - k * period) -
                                trans_duration <= jitter_requirement)
                formula.append(constraint_9)
                

    
    
    
    
    
    
    
    

    return formula


def _main():
    
    
    
    (link_obj_set,
     stream_obj_set,
     stream_instance_obj_set) = init_topo_and_stream_obj_set_for_window_demo('../topo_test', '../stream_test')

    construct_constraints_for_window_demo(link_obj_set,
                                          stream_obj_set,
                                          stream_instance_obj_set,
                                          sync_precision=1)
    return


if __name__ == '__main__':
    _main()
