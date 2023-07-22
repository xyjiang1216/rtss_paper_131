from random import randint, choice
import matplotlib.pyplot as plt
import networkx as nx








from lib.txt_engine import write_topo_or_stream_to_txt


def _show_topology_graph(graph):
    pos = nx.spring_layout(graph, iterations=200)  
    nx.draw(graph, pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'link_id')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    
    plt.show(block=True)
    
    
    plt.close('all')





def _generate_linear_topo_graph(sw_num,
                                es_num_per_sw_set,
                                show_topo_graph):
    
    G = nx.DiGraph()

    
    sw_id = 0
    for sw in range(sw_num):
        G.add_node(sw_id, node_id=sw_id, node_type='SW', es_set=[])
        sw_id += 1

    
    es_id = sw_num
    for sw in range(sw_num):
        es_num_of_current_sw = choice(es_num_per_sw_set)
        for es in range(es_num_of_current_sw):
            G.add_node(es_id, node_id=es_id, node_type='ES')
            
            es_set = G.nodes[sw]['es_set']
            es_set.append(es_id)
            G.nodes[sw]['es_set'] = es_set
            es_id += 1

    
    sw_id_set = range(0, sw_num)
    link_id = 0
    for sw in sw_id_set[0:-1]:
        G.add_edge(sw, sw + 1, link_id=link_id)
        link_id += 1
        G.add_edge(sw + 1, sw, link_id=link_id)
        link_id += 1

    
    for sw in sw_id_set:
        es_set = G.nodes[sw]['es_set']
        print(es_set)
        for es in es_set:
            G.add_edge(sw, es, link_id=link_id)
            link_id += 1
            G.add_edge(es, sw, link_id=link_id)
            link_id += 1

    
    if show_topo_graph:
        _show_topology_graph(G)

    print(G)
    
    return G





def _generate_ring_topo_graph(sw_num,
                              es_num_per_sw_set,
                              show_topo_graph):
    
    G = nx.DiGraph()

    
    sw_id = 0
    for sw in range(sw_num):
        G.add_node(sw_id, node_id=sw_id, node_type='SW', es_set=[])
        sw_id += 1

    
    es_id = sw_num
    for sw in range(sw_num):
        es_num_of_current_sw = choice(es_num_per_sw_set)
        for es in range(es_num_of_current_sw):
            G.add_node(es_id, node_id=es_id, node_type='ES')
            
            es_set = G.nodes[sw]['es_set']
            es_set.append(es_id)
            G.nodes[sw]['es_set'] = es_set
            es_id += 1

    
    sw_id_set = range(0, sw_num)
    link_id = 0
    for sw in sw_id_set:
        G.add_edge(sw, (sw + 1) % sw_num, link_id=link_id)
        link_id += 1
        G.add_edge((sw + 1) % sw_num, sw, link_id=link_id)
        link_id += 1

    
    for sw in sw_id_set:
        es_set = G.nodes[sw]['es_set']
        print(es_set)
        for es in es_set:
            G.add_edge(sw, es, link_id=link_id)
            link_id += 1
            G.add_edge(es, sw, link_id=link_id)
            link_id += 1

    
    if show_topo_graph:
        _show_topology_graph(G)

    print(G)
    
    return G





def _generate_snowflake_topo_graph(sw_num,
                                   es_num_per_sw_set,
                                   show_topo_graph,
                                   ):
    
    G = nx.DiGraph()

    
    sw_id = 0
    link_id = 0
    
    G.add_node(sw_id, node_id=sw_id, node_type='SW', es_set=[])
    sw_id += 1

    former_node_num = 1
    last_layer_sw_id_set = []
    former_layer_sw_id_set = [0]
    cnt_layer_sw_id_set = []
    
    
    if len(es_num_per_sw_set) == 1:
        last_layer_sw_id_set.append(0)
    
    elif len(es_num_per_sw_set) >= 2:
        last_layer_sw_idx = 0
        for num_per_node in es_num_per_sw_set[:-1]:
            for former_sw_id in former_layer_sw_id_set:
                for i in range(num_per_node):
                    G.add_node(sw_id, node_id=sw_id, node_type='SW', es_set=[])
                    cnt_layer_sw_id_set.append(sw_id)
                    if last_layer_sw_idx == len(es_num_per_sw_set) - 2:
                        last_layer_sw_id_set.append(sw_id)

                    G.add_edge(former_sw_id, sw_id, link_id=link_id)
                    link_id += 1
                    G.add_edge(sw_id, former_sw_id, link_id=link_id)
                    link_id += 1

                    sw_id += 1
            former_layer_sw_id_set = cnt_layer_sw_id_set
            cnt_layer_sw_id_set = []
            last_layer_sw_idx += 1

    
    
    es_id = sw_id
    
    es_node_num = former_node_num * es_num_per_sw_set[-1]
    
    for sw_id in last_layer_sw_id_set:
        for es in range(es_num_per_sw_set[-1]):
            G.add_node(es_id, node_id=es_id, node_type='ES')

            G.add_edge(sw_id, es_id, link_id=link_id)
            link_id += 1
            G.add_edge(es_id, sw_id, link_id=link_id)
            link_id += 1

            es_id += 1

    
    if show_topo_graph:
        _show_topology_graph(G)

    print(G)
    
    return G





def _generate_topology(sw_num,
                       es_num_per_sw_set,
                       speed_set,  
                       st_queues_set,  
                       topo_type,
                       **kwargs  
                       ):
    """

    :param sw_num: 如果拓扑类型是雪花型，这个参数表示雪花层数
    :param es_num_per_sw_set: 如果拓扑类型是雪花型，这个参数表示每层的雪花数量
    :param speed_set:
    :param st_queues_set:
    :param topo_type:
    :param kwargs:
    :return:
    """
    
    if kwargs.get('show_topo_graph') is None:
        show_topo_graph = False
    else:
        show_topo_graph = kwargs['show_topo_graph']

    if kwargs.get('macrotick') is not None and kwargs.get('gcl_len') is not None:
        print("Error - More than one parameter entered. "
              "Only one of gcl_len or macrotick can be selected.")
        exit(0)

    
    
    
    
    
    

    G = None
    topo_set = []
    if topo_type == 'linear':
        G = _generate_linear_topo_graph(sw_num, es_num_per_sw_set, show_topo_graph)
    elif topo_type == 'ring':
        G = _generate_ring_topo_graph(sw_num, es_num_per_sw_set, show_topo_graph)
    elif topo_type == 'snowflake':
        G = _generate_snowflake_topo_graph(sw_num, es_num_per_sw_set, show_topo_graph)
    else:
        print('Error - invalid topo_type')
        exit(0)

    links = G.edges
    for per_link in links:
        src_node = per_link[0]
        dst_node = per_link[1]
        link_id = G[src_node][dst_node]['link_id']
        speed = choice(speed_set)
        st_queues = choice(st_queues_set)
        
        
        
        link = {}
        
        if kwargs.get('macrotick') is not None and \
                kwargs.get('macrotick') > 0:
            
            macrotick = kwargs['macrotick']
            link = {'link_id': link_id, 'src_node': src_node,
                    'dst_node': dst_node, 'speed': speed,
                    'st_queues': st_queues, 'macrotick': macrotick
                    }
        
        elif kwargs.get('gcl_len') is not None and \
                kwargs.get('gcl_len') > 0:
            
            gcl_len = kwargs['gcl_len']
            link = {'link_id': link_id, 'src_node': src_node,
                    'dst_node': dst_node, 'speed': speed,
                    'st_queues': st_queues, 'gcl_len': gcl_len
                    }
        
        else:
            
            
            
            link = {'link_id': link_id, 'src_node': src_node,
                    'dst_node': dst_node, 'speed': speed,
                    'st_queues': st_queues
                    }
        topo_set.append(link)
    topo_set.sort(key=lambda x: x['link_id'])
    return G, topo_set





def _random_route_path_for_streams(G, stream_num,
                                   max_hop):
    route_path_set = []
    
    es_node = []
    for node in G.nodes:
        if G.nodes[node]['node_type'] == 'ES':
            es_id = G.nodes[node]['node_id']
            
            es_node.append(es_id)
    
    stream = 0
    while stream < stream_num:
        
        src_es_id = choice(es_node)
        dst_es_id = choice(es_node)
        while dst_es_id == src_es_id:
            dst_es_id = choice(es_node)

        shortest_path_in_node_id = nx.shortest_path(G, src_es_id, dst_es_id)
        
        if len(shortest_path_in_node_id) > max_hop + 1:
            continue
        
        
        shortest_path_in_link_id = []
        for src_node_id, dst_node_id in zip(shortest_path_in_node_id, shortest_path_in_node_id[1:]):
            link_id = G[src_node_id][dst_node_id]['link_id']
            shortest_path_in_link_id.append(link_id)
        route_path_set.append(shortest_path_in_link_id)
        stream += 1
    return route_path_set







def _generate_random_streams(G,
                             stream_num,
                             size_set,
                             period_set,
                             latency_requirement_set,
                             jitter_requirement_set,
                             max_hop):
    stream_set = []
    
    route_set = _random_route_path_for_streams(G, stream_num,
                                               max_hop)

    for (stream_id, route) in zip(range(stream_num), route_set):
        size = choice(size_set)
        index = randint(0, len(period_set) - 1)
        period = period_set[index]
        latency_requirement = latency_requirement_set[index]
        jitter_requirement = jitter_requirement_set[index]
        stream = {'stream_id': stream_id,
                  'size': size,
                  'period': period,
                  'latency_requirement': latency_requirement,
                  'jitter_requirement': jitter_requirement,
                  'route': route}
        stream_set.append(stream)
    return stream_set






def construct_topo_and_streams(topo_txt,
                               stream_txt,
                               topo_type='linear',
                               sw_num=5,
                               es_num_per_sw_set=None,
                               speed_set=None,
                               st_queues_set=None,
                               stream_num=50,
                               size_set=None,
                               period_set=None,
                               latency_requirement_set=None,
                               jitter_requirement_set=None,
                               max_hop=7,
                               **kwargs):  
    """

    :param topo_txt:
    :param stream_txt:
    :param topo_type: 默认为线性，目前暂不支持其他类型的拓扑
    :param sw_num:
    :param es_num_per_sw_set:
    :param speed_set:
    :param st_queues_set:
    :param stream_num:
    :param size_set:
    :param period_set:
    :param latency_requirement_set:
    :param jitter_requirement_set:
    :param max_hop: 默认为7
    :param kwargs:
    :return:
    """

    if es_num_per_sw_set is None:
        es_num_per_sw_set = [2]
    if speed_set is None:
        speed_set = [1000]
    if st_queues_set is None:
        st_queues_set = [2]
    if size_set is None:
        size_set = [1518]
    if period_set is None:
        period_set = [20000]
    if latency_requirement_set is None:
        latency_requirement_set = [20000]
    if jitter_requirement_set is None:
        jitter_requirement_set = [200]

    
    G, topo_set = _generate_topology(sw_num,
                                     es_num_per_sw_set,
                                     speed_set,
                                     st_queues_set,
                                     topo_type,
                                     **kwargs
                                     )

    
    write_topo_or_stream_to_txt(topo_txt, topo_set)

    
    stream_set = _generate_random_streams(G, stream_num, size_set,
                                          period_set,
                                          latency_requirement_set,
                                          jitter_requirement_set,
                                          max_hop)
    
    write_topo_or_stream_to_txt(stream_txt, stream_set)

    return


def _main():
    construct_topo_and_streams('../log/topo_test',
                               '../log/stream_test',
                               topo_type='snowflake',
                               sw_num=5,
                               es_num_per_sw_set=[3, 3, 2],
                               speed_set=[1000],
                               st_queues_set=[2],
                               stream_num=75,
                               size_set=[1518],
                               period_set=[20000],
                               latency_requirement_set=[20000],
                               jitter_requirement_set=[200],
                               gcl_len=1,
                               show_topo_graph=True)
    return


if __name__ == '__main__':
    _main()
