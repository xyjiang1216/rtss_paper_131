import math

from lib.Lib import compute_cycle_period
from lib.txt_engine import read_topo_or_streams_from_txt


def init_raster_candidate(topo_txt, stream_txt,
                          bandwidth,
                          max_d,
                          sync_precision):
    raster_candidate = []

    # BD
    # max(d)
    # delta
    # max(C_i)
    # T_S
    # oc_i

    stream_set = read_topo_or_streams_from_txt(stream_txt)
    max_frame_size = 0
    for stream in stream_set:
        if stream['size'] > max_frame_size:
            max_frame_size = stream['size']

    period_set = []
    for stream in stream_set:
        period_set.append(stream['period'])
    hyper_period = compute_cycle_period(*period_set)

    total_occurrence = 0
    for stream in stream_set:
        total_occurrence += math.ceil(hyper_period / stream['period'])

    # print(max_frame_size)
    # print(hyper_period)
    # print(total_occurrence)

    max_raster = math.floor(hyper_period / total_occurrence)
    min_raster = math.ceil(max_frame_size*8 / bandwidth + max_d + sync_precision)

    for raster in range(min_raster, max_raster + 1):
        flag = 'common divisor'
        for stream in stream_set:
            if stream['period'] % raster != 0:
                flag = 'not common divisor'
                break
        if flag == 'common divisor':
            raster_candidate.append(raster)

    # print(raster_candidate)
    # print(min_raster)
    # print(max_raster)

    return raster_candidate
