from RAP_demo.data_structure_for_RAP_demo import Link, Stream, Stream_Instance
from lib.txt_engine import read_topo_or_streams_from_txt






def _init_link_obj_set_for_RAP_demo(topo_txt):
    topo_set = read_topo_or_streams_from_txt(topo_txt)
    
    link_obj_set = []
    for link in topo_set:
        link_obj = Link(link_id=link['link_id'],
                        src_node=link['src_node'],
                        dst_node=link['dst_node'],
                        
                        st_queues=link['st_queues'],
                        
                        )
        link_obj_set.append(link_obj)
    
    return link_obj_set


def _init_stream_obj_set_for_RAP_demo(stream_txt, link_obj_set):
    stream_set = read_topo_or_streams_from_txt(stream_txt)
    stream_obj_set = []
    
    for stream in stream_set:
        hop_id = 0
        for link_id in stream['route']:
            link_obj_set[link_id].add_stream_to_current_link(stream['stream_id'], hop_id)
            hop_id += 1
        stream_obj = Stream(stream_id=stream['stream_id'],
                            size=stream['size'],
                            period=stream['period'],
                            latency_requirement=stream['latency_requirement'],
                            jitter_requirement=stream['jitter_requirement'],
                            route_set=stream['route'])
        stream_obj_set.append(stream_obj)
    return stream_obj_set


def _init_stream_instance_obj_set_for_RAP_demo(stream_obj_set, link_obj_set,
                                               raster):
    stream_instance_obj_set = []
    for stream_obj in stream_obj_set:
        stream_instance_obj_set_per_stream = []
        period = stream_obj.period / raster
        route_set = stream_obj.route_set
        hop_id = 0
        stream_id = stream_obj.stream_id
        size = stream_obj.size
        for link_id in route_set:
            
            
            
            stream_instance_obj = Stream_Instance(stream_id=stream_id,
                                                  link_id=link_id,
                                                  hop_id=hop_id,
                                                  period_scaled_to_raster=period,
                                                  
                                                  )
            
            hop_id += 1
            stream_instance_obj_set_per_stream.append(stream_instance_obj)
        stream_instance_obj_set.append(stream_instance_obj_set_per_stream)
    return stream_instance_obj_set


def init_topo_and_stream_obj_set_for_RAP_demo(topo_txt, stream_txt, raster):
    link_obj_set = _init_link_obj_set_for_RAP_demo(topo_txt)
    stream_obj_set = _init_stream_obj_set_for_RAP_demo(stream_txt, link_obj_set)
    stream_instance_obj_set = _init_stream_instance_obj_set_for_RAP_demo(stream_obj_set,
                                                                         link_obj_set,
                                                                         raster)
    return link_obj_set, stream_obj_set, stream_instance_obj_set


def _main():
    raster = 12
    init_topo_and_stream_obj_set_for_RAP_demo('../topo_test', '../stream_test',
                                              raster)
    return


if __name__ == '__main__':
    _main()
    pass
