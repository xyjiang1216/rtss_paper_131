from window_demo.constraints_constructor_for_window_demo import *
from window_demo.topo_and_streams_txt_parser_for_window_demo import *
from window_demo.z3_model_parser_for_window_demo import *
from lib.z3_constraints_solver import *
from lib.topo_and_streams_generator import *


def main():
    print('1: generating topo and stream txt...')
    construct_topo_and_streams('../log/topo_win_4_stream_200',
                               '../log/stream_win_4_stream_200',
                               sw_num=5,
                               es_num_per_sw_set=[3],
                               speed_set=[1000],
                               st_queues_set=[4],
                               stream_num=200,
                               size_set=[1518],
                               period_set=[10000, 20000],
                               latency_requirement_set=[10000, 20000],
                               jitter_requirement_set=[100, 200],
                               gcl_len=4,
                               show_topo_graph=False)

    print('2: initializing topo and stream object set...')
    (link_obj_set,
     stream_obj_set,
     stream_instance_obj_set) = init_topo_and_stream_obj_set_for_window_demo('../log/topo_win_4_stream_200',
                                                                             '../log/stream_win_4_stream_200')

    print('3: constructing constraints...')
    constraint_set = construct_constraints_for_window_demo(link_obj_set,
                                                           stream_obj_set,
                                                           stream_instance_obj_set,
                                                           sync_precision=1)

    print('4: adding and solving constraints...')
    result_set = add_and_solve_constraints(constraint_set, timeout=3 * 60 * 60 * 1000)
    print(result_set)

    print('5: writing solution...')
    write_declare_set_to_txt(result_set, link_obj_set, '../log/solution_win_4_stream_200')

    return


if __name__ == '__main__':
    main()
