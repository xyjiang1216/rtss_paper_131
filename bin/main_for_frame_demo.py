from frame_demo.constraints_constructor_for_frame_demo import construct_constraints_for_frame_demo
from frame_demo.topo_and_streams_txt_parser_for_frame_demo import init_topo_and_stream_obj_set_for_frame_demo
from frame_demo.z3_model_parser_for_frame_demo import write_declare_set_to_txt
from lib.topo_and_streams_generator import construct_topo_and_streams
from lib.z3_constraints_solver import add_and_solve_constraints


def main():
    print('1: generating topo and stream txt...')
    construct_topo_and_streams('../log/topo_macrotick_1_stream_200',
                               '../log/stream_macrotick_1_stream_200',
                               sw_num=5,
                               es_num_per_sw_set=[3],
                               speed_set=[1000],
                               st_queues_set=[4],
                               stream_num=250,
                               size_set=[1518],
                               period_set=[10000, 20000],
                               latency_requirement_set=[10000, 20000],
                               jitter_requirement_set=[100, 200],
                               macrotick=1,
                               show_topo_graph=False)

    print('2: initializing topo and stream object set...')
    (link_obj_set,
     stream_obj_set,
     stream_instance_obj_set) = init_topo_and_stream_obj_set_for_frame_demo('../log/topo_macrotick_1_stream_200',
                                                                            '../log/stream_macrotick_1_stream_200', )

    print('3: constructing constraints...')
    constraint_formula_set = construct_constraints_for_frame_demo(link_obj_set,
                                                                  stream_obj_set,
                                                                  stream_instance_obj_set,
                                                                  sync_precision=1)

    print('4: adding and solving constraints...')
    result_set = add_and_solve_constraints(constraint_formula_set, timeout=-1)

    print('5: writing solution...')
    write_declare_set_to_txt(result_set, link_obj_set, '../log/solution_macrotick_1_stream_200')

    return


if __name__ == '__main__':
    main()
