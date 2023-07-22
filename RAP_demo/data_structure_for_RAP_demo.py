import math
from z3 import *

transDelay_min = 3
transDelay_max = 5

bandwidth = 1000


class Link:
    def __init__(self, link_id, src_node, dst_node,

                 st_queues):
        self.link_id = link_id
        self.src_node = src_node
        self.dst_node = dst_node

        self.st_queues = st_queues

        self.stream_set = []

    def add_stream_to_current_link(self, stream_id, hop_id):
        self.stream_set.append({'stream_id': stream_id, 'hop_id': hop_id})


class Stream:
    def __init__(self,
                 stream_id,
                 size,
                 period,
                 latency_requirement,
                 jitter_requirement,
                 route_set):
        self.stream_id = stream_id
        self.size = size
        self.period = period
        self.latency_requirement = latency_requirement
        self.jitter_requirement = jitter_requirement

        self.route_set = route_set


class Stream_Instance:
    def __init__(self,
                 stream_id,
                 link_id,
                 hop_id,
                 period_scaled_to_raster,

                 ):
        self.stream_id = stream_id
        self.link_id = link_id

        self.hop_id = hop_id

        self.period_scaled_to_raster = period_scaled_to_raster

        self.omega = Int(f'O_{stream_id}^({link_id})')
        self.rho = Int(f'P_{stream_id}^({link_id})')


if __name__ == '__main__':
    pass
