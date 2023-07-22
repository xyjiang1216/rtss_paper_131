from z3 import *





class Link:
    def __init__(self, link_id, src_node, dst_node,
                 speed, gcl_len, st_queues):
        self.link_id = link_id  
        self.src_node = src_node
        self.dst_node = dst_node
        self.speed = speed  
        self.gcl_len = gcl_len  
        self.st_queues = st_queues  

        
        
        
        
        
        self.phi_array = Array(f'P^({link_id})', IntSort(), IntSort())
        
        self.tau_array = Array(f'T^({link_id})', IntSort(), IntSort())
        
        self.tau_0_array = Array(f'T_0^({link_id})', IntSort(), IntSort())
        
        self.tau_1_array = Array(f'T_1^({link_id})', IntSort(), IntSort())
        
        self.kappa_array = Array(f'K^({link_id})', IntSort(), IntSort())

        
        
        self.stream_set = []

    def add_stream_to_current_link(self, stream_id, hop_id):
        self.stream_set.append({'stream_id': stream_id, 'hop_id': hop_id})



class Route:
    def __init__(self, link_id):
        self.link_id = link_id
        self.trans_duration = 0

    
    def compute_trans_duration(self, size, speed):
        self.trans_duration = math.ceil(size * 8 / speed)
        



class Stream:
    def __init__(self, stream_id, size, period,
                 latency_requirement, jitter_requirement,
                 route_obj_set):
        self.stream_id = stream_id
        self.size = size
        self.period = period
        self.latency_requirement = latency_requirement
        self.jitter_requirement = jitter_requirement
        
        self.route_obj_set = route_obj_set




class Stream_Instance:
    
    
    
    def __init__(self, stream_id, link_id,
                 instance_id, hop_id):
        self.stream_id = stream_id
        self.link_id = link_id
        self.instance_id = instance_id
        
        self.hop_id = hop_id
        
        
        
        
        
        self.omega = Int(f'O_{stream_id},{instance_id}^({link_id})')


if __name__ == '__main__':
    pass
