import time

from z3 import *

from RAP_demo.topo_and_streams_txt_parser_for_RAP_demo import init_topo_and_stream_obj_set_for_RAP_demo
from lib.Lib import compute_cycle_period


def construct_constraints_for_RAP_demo(
        raster,
        link_obj_set,
        stream_obj_set,
        stream_instance_obj_set,
        sync_precision=1, ):
    constraint_formula_set = []

    start = time.time_ns()
    # 1. contention-free constraint
    for link in link_obj_set:
        stream_set = link.stream_set

        for i in range(len(stream_set)):
            for j in range(len(stream_set)):
                if i != j:
                    i_stream_id = stream_set[i]['stream_id']
                    i_hop_id = stream_set[i]['hop_id']
                    j_stream_id = stream_set[j]['stream_id']
                    j_hop_id = stream_set[j]['hop_id']
                    i_omega = stream_instance_obj_set[i_stream_id][i_hop_id].omega
                    i_period_scaled_to_raster = stream_instance_obj_set[i_stream_id][
                        i_hop_id].period_scaled_to_raster

                    j_omega = stream_instance_obj_set[j_stream_id][j_hop_id].omega
                    j_period_scaled_to_raster = stream_instance_obj_set[j_stream_id][
                        j_hop_id].period_scaled_to_raster

                    i_period = stream_obj_set[i_stream_id].period
                    j_period = stream_obj_set[j_stream_id].period

                    i_j_cycle_period = compute_cycle_period(*[i_period, j_period])

                    for k in range(math.ceil(i_j_cycle_period / i_period)):
                        for l in range(math.ceil(i_j_cycle_period / j_period)):
                            formula = (i_omega + k * i_period_scaled_to_raster !=
                                       j_omega + l * j_period_scaled_to_raster)
                            constraint_formula_set.append(formula)
    end = time.time_ns()
    time_used_in_second = (end - start) / 1000000000

    start = time.time_ns()
    # 2. Zero aggregation constraint
    for link in link_obj_set:
        stream_set = link.stream_set
        link_id = link.link_id

        for i in range(len(stream_set)):
            for j in range(len(stream_set)):
                if i != j:
                    i_stream_id = stream_set[i]['stream_id']
                    i_ab_hop_id = stream_set[i]['hop_id']
                    j_stream_id = stream_set[j]['stream_id']
                    j_ab_hop_id = stream_set[j]['hop_id']
                    if i_ab_hop_id != 0 and j_ab_hop_id != 0:

                        i_xa_hop_id = stream_set[i]['hop_id'] - 1
                        j_ya_hop_id = stream_set[j]['hop_id'] - 1

                        j_ab_omega = stream_instance_obj_set[j_stream_id][j_ab_hop_id].omega
                        j_ya_omega = stream_instance_obj_set[j_stream_id][j_ya_hop_id].omega

                        j_period = stream_obj_set[j_stream_id].period
                        i_period = stream_obj_set[i_stream_id].period

                        i_xa_omega = stream_instance_obj_set[i_stream_id][i_xa_hop_id].omega

                        i_ab_omega = stream_instance_obj_set[i_stream_id][i_ab_hop_id].omega

                        xa_link_id = stream_instance_obj_set[i_stream_id][i_xa_hop_id].link_id

                        ya_link_id = stream_instance_obj_set[j_stream_id][j_ya_hop_id].link_id

                        i_ab_rho = stream_instance_obj_set[i_stream_id][i_ab_hop_id].rho
                        j_ab_rho = stream_instance_obj_set[j_stream_id][j_ab_hop_id].rho

                        formula = Bool('p')

                        i_j_cycle_period = compute_cycle_period(*[i_period, j_period])

                        for k in range(int(math.ceil(i_j_cycle_period / i_period))):
                            for l in range(math.ceil(i_j_cycle_period / j_period)):
                                formula = And(formula,
                                              Or(
                                                  j_ab_omega +
                                                  l * j_period / raster
                                                  !=
                                                  i_xa_omega +
                                                  k * i_period / raster
                                              ))

                        formula = Or(formula,
                                     i_ab_rho != j_ab_rho)

                        constraint_formula_set.append(formula)

    end = time.time_ns()
    time_used_in_second = (end - start) / 1000000000

    start = time.time_ns()
    # 3. queue resource constraint
    for stream_instance_set in stream_instance_obj_set:
        for stream_instance in stream_instance_set:
            link_id = stream_instance.link_id
            formula = (stream_instance.rho < link_obj_set[link_id].st_queues,
                       stream_instance.rho >= 0)
            constraint_formula_set.append(formula)

    end = time.time_ns()
    time_used_in_second = (end - start) / 1000000000

    start = time.time_ns()
    # 4. sequence constraint
    for stream_instance_obj in stream_instance_obj_set:
        for i in range(len(stream_instance_obj) - 1):
            ax_link_id = stream_instance_obj[i].link_id
            xb_link_id = stream_instance_obj[i + 1].link_id

            xb_omega = stream_instance_obj[i + 1].omega
            ax_omega = stream_instance_obj[i].omega

            formula = (xb_omega -
                       ax_omega >=
                       1)
            constraint_formula_set.append(formula)

    end = time.time_ns()
    time_used_in_second = (end - start) / 1000000000

    start = time.time_ns()
    # 5. period constraint
    for stream_instance_obj_set_per_stream in stream_instance_obj_set:
        for stream_instance_obj in stream_instance_obj_set_per_stream:
            formula = And(stream_instance_obj.omega >= 0,
                          stream_instance_obj.omega <
                          stream_instance_obj.period_scaled_to_raster)

            constraint_formula_set.append(formula)

    end = time.time_ns()
    time_used_in_second = (end - start) / 1000000000

    start = time.time_ns()
    # 6. end-to-end constraint
    stream_id = 0
    for stream_instance_obj_set_per_stream in stream_instance_obj_set:
        latency_requirement = stream_obj_set[stream_id].latency_requirement
        src_omega = stream_instance_obj_set_per_stream[0].omega
        src_link_id = stream_instance_obj_set_per_stream[0].link_id

        dst_omega = stream_instance_obj_set_per_stream[-1].omega
        dst_link_id = stream_instance_obj_set_per_stream[-1].link_id

        formula = ((dst_omega - src_omega + 1) * raster + sync_precision <=
                   latency_requirement)
        constraint_formula_set.append(formula)

        stream_id += 1

    end = time.time_ns()
    time_used_in_second = (end - start) / 1000000000

    return constraint_formula_set


def _main():
    raster = 12
    (link_obj_set,
     stream_obj_set,
     stream_instance_obj_set) = init_topo_and_stream_obj_set_for_RAP_demo(raster,
                                                                          '../topo_test',
                                                                          '../stream_test')

    construct_constraints_for_RAP_demo(raster,
                                       link_obj_set,
                                       stream_obj_set,
                                       stream_instance_obj_set,
                                       sync_precision=1)
    return


if __name__ == '__main__':
    _main()
