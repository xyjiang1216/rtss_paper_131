from RAP_demo.constraints_constructor_for_RAP_demo import construct_constraints_for_RAP_demo
from RAP_demo.topo_and_streams_txt_parser_for_RAP_demo import init_topo_and_stream_obj_set_for_RAP_demo
from RAP_demo.z3_model_parser_for_RAP_demo import write_declare_set_to_txt
from lib.topo_and_streams_generator import construct_topo_and_streams
from lib.z3_constraints_solver import add_and_solve_constraints


def main():



    print('1: generating topo and stream txt...')
    construct_topo_and_streams('../log/topo_for_RAP_demo',
                               '../log/stream_for_RAP_demo',
                               sw_num=2,
                               es_num_per_sw_set=[1],
                               speed_set=[1000],
                               st_queues_set=[1],
                               stream_num=20,
                               size_set=[1500],
                               period_set=[20000],
                               latency_requirement_set=[20000],
                               jitter_requirement_set=[200],
                               show_topo_graph=False)

    # Phase I
    raster = 10

    print('2: initializing topo and stream object set...')
    (link_obj_set,
     stream_obj_set,
     stream_instance_obj_set) = init_topo_and_stream_obj_set_for_RAP_demo('../log/topo_for_RAP_demo',
                                                                          '../log/stream_for_RAP_demo',
                                                                          raster=raster
                                                                          )

    # Phase II
    print('3: constructing constraints...')
    constraint_formula_set = construct_constraints_for_RAP_demo(raster,
                                                                link_obj_set,
                                                                stream_obj_set,
                                                                stream_instance_obj_set,
                                                                sync_precision=0.048)

    print('4: adding and solving constraints...')
    result_set = add_and_solve_constraints(constraint_formula_set, timeout=10 * 60 * 1000)

    print('5: writing solution...')
    write_declare_set_to_txt(result_set, link_obj_set, '../log/solution_RAP_demo')


if __name__ == '__main__':
    main()
