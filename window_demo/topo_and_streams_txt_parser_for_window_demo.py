from window_demo.data_structure_for_window_demo import *
from lib.txt_engine import read_topo_or_streams_from_txt
from lib.Lib import compute_cycle_period






def _init_link_obj_set_for_window_demo(topo_txt):
    topo_set = read_topo_or_streams_from_txt(topo_txt)
    
    link_obj_set = []
    for link in topo_set:
        link_obj = Link(link_id=link['link_id'],
                        src_node=link['src_node'],
                        dst_node=link['dst_node'],
                        speed=link['speed'],
                        st_queues=link['st_queues'],
                        gcl_len=link['gcl_len'])
        link_obj_set.append(link_obj)
    return link_obj_set


def _init_stream_obj_set_for_window_demo(stream_txt, link_obj_set):
    stream_set = read_topo_or_streams_from_txt(stream_txt)
    stream_obj_set = []
    
    
    for stream in stream_set:
        route_obj_set = []
        hop_id = 0
        
        for link_id in stream['route']:
            
            route_obj = Route(link_id)
            size = stream['size']
            speed = link_obj_set[link_id].speed
            route_obj.compute_trans_duration(size, speed)
            route_obj_set.append(route_obj)
            
            link_obj_set[link_id].add_stream_to_current_link(stream['stream_id'], hop_id)
            hop_id += 1
        stream_obj = Stream(stream_id=stream['stream_id'],
                            size=stream['size'],
                            period=stream['period'],
                            latency_requirement=stream['latency_requirement'],
                            jitter_requirement=stream['jitter_requirement'],
                            route_obj_set=route_obj_set)
        stream_obj_set.append(stream_obj)
    return stream_obj_set


def _init_stream_instance_obj_set_for_window_demo(stream_obj_set):
    period_set = []
    for stream_obj in stream_obj_set:
        period_set.append(stream_obj.period)
    hyper_period = compute_cycle_period(*period_set)
    
    stream_instance_obj_set = []
    for stream_obj in stream_obj_set:
        stream_instance_obj_set_per_stream = []
        stream_id = stream_obj.stream_id
        period = stream_obj.period
        route_obj_set = stream_obj.route_obj_set
        hop_id = 0
        for route_obj in route_obj_set:
            stream_instance_obj_set_per_route = []
            link_id = route_obj.link_id
            for instance_id in range(math.ceil(hyper_period / period)):
                stream_instance_obj = Stream_Instance(stream_id=stream_id,
                                                      link_id=link_id,
                                                      instance_id=instance_id,
                                                      hop_id=hop_id)
                stream_instance_obj_set_per_route.append(stream_instance_obj)
            stream_instance_obj_set_per_stream.append(stream_instance_obj_set_per_route)
            hop_id += 1
        stream_instance_obj_set.append(stream_instance_obj_set_per_stream)

    return stream_instance_obj_set


def init_topo_and_stream_obj_set_for_window_demo(topo_txt, stream_txt):
    link_obj_set = _init_link_obj_set_for_window_demo(topo_txt)
    stream_obj_set = _init_stream_obj_set_for_window_demo(stream_txt, link_obj_set)
    stream_instance_obj_set = _init_stream_instance_obj_set_for_window_demo(stream_obj_set)
    return link_obj_set, stream_obj_set, stream_instance_obj_set



def _main():
    
    
    
    
    
    
    
    
    
    
    
    
    return


if __name__ == '__main__':
    _main()
    pass
