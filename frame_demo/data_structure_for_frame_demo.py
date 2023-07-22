import math
from z3 import *





class Link:
    def __init__(self, link_id, src_node, dst_node,
                 speed,
                 macrotick,
                 st_queues):
        self.link_id = link_id  
        self.src_node = src_node
        self.dst_node = dst_node
        self.speed = speed  
        self.macrotick = macrotick
        self.st_queues = st_queues  
        
        
        
        
        
        self.stream_set = []

    def add_stream_to_current_link(self, stream_id, hop_id):
        self.stream_set.append({'stream_id': stream_id, 'hop_id': hop_id})


class Stream:
    def __init__(self, stream_id, size, period, latency_requirement, route_set):
        self.stream_id = stream_id
        self.size = size
        self.period = period
        self.latency_requirement = latency_requirement
        
        self.route_set = route_set





class Stream_Instance:
    def __init__(self,
                 stream_id,
                 link_id,
                 hop_id,
                 period,
                 trans_duration):
        self.stream_id = stream_id
        self.link_id = link_id
        
        self.hop_id = hop_id
        
        
        
        self.period_scaled_to_macrotick = period
        self.trans_duration_scaled_to_macrotick = trans_duration
        
        
        
        self.offset = Int(f'O_{stream_id}^({link_id})')
        self.prio = Int(f'P_{stream_id}^({link_id})')

    def init_period_and_trans_duration(self, macrotick):
        self.period_scaled_to_macrotick = math.ceil(self.period_scaled_to_macrotick / macrotick)
        self.trans_duration_scaled_to_macrotick = math.ceil(self.trans_duration_scaled_to_macrotick /
                                                            macrotick)


if __name__ == '__main__':
    pass
