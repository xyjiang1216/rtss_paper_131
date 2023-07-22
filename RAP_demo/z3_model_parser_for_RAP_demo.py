from z3 import *
import re








def _classify_declare_set(declare_set, link_num):
    tmp_declare_set = [{'omega_set': [], 'queue_set': []} for link_id in range(link_num)]

    
    
    
    for declare in declare_set:
        name = declare['name']
        value = declare['value']
        value = str(value)

        if re.match(r'O.', name):
            
            link_id = int(name.split('(')[1].split(')')[0])
            declare['value'] = int(value)
            tmp_declare_set[link_id]['omega_set'].append(declare)
        elif re.match(r'P.', name):
            
            link_id = int(name.split('(')[1].split(')')[0])
            declare['value'] = int(value)
            tmp_declare_set[link_id]['queue_set'].append(declare)

    declare_set = tmp_declare_set

    
    
    
    for declare_set_per_link in declare_set:
        omega_set = declare_set_per_link['omega_set']
        queue_set = declare_set_per_link['queue_set']
        tmp_queue_set = [''] * len(omega_set)

        for queue in queue_set:
            name = queue['name']
            
            queue_stream_id = name.split('_')[1].split('^')[0]
            idx = 0
            for omega in omega_set:
                omega_stream_id = omega['name'].split('_')[1].split('^')[0]
                if queue_stream_id == omega_stream_id:
                    break
                idx += 1
            
            tmp_queue_set[idx] = queue

        declare_set_per_link['queue_set'] = tmp_queue_set
    return declare_set


def _sort_declare_set(declare_set):
    
    for declare in declare_set:
        omega_set = declare['omega_set']
        queue_set = declare['queue_set']
        if omega_set and queue_set:
            
            
            zipped_set = zip(omega_set, queue_set)
            
            sorted_zipped_set = sorted(zipped_set, key=lambda tmp: (tmp[0]['value'], tmp[1]['value']))
            sorted_set = zip(*sorted_zipped_set)
            
            
            
            declare['omega_set'], declare['queue_set'] = [list(x) for x in sorted_set]
    
    return declare_set


def _format_omega_set_and_rho_set(f, declare, width):
    omega_set = declare['omega_set']
    queue_set = declare['queue_set']

    f.write('-' * (width - 1) + '|' + '\n')
    for omega, queue in zip(omega_set, queue_set):
        f.write('{:>15}{:^20}{}{:^15}{}\n'.format('omega:', omega['name'], '=', omega['value'], '|'))
        f.write('{:>15}{:^20}{}{:^15}{}\n'.format('rho:', queue['name'], '=', queue['value'], '|'))
        f.write('-' * (width - 1) + '|' + '\n')


def _write_time_used_to_txt(f, time_used_in_second):
    divider = '+' * 80
    f.write('%s\n' % divider)
    f.write('time used:\n')
    f.write("%s s\n" % time_used_in_second)
    f.write("%s min\n" % (time_used_in_second / 60))
    return


def write_declare_set_to_txt(result_set,
                             link_obj_set,
                             solution_txt
                             ):
    time_used_in_second = result_set['time_used_in_second']
    sat_or_not = result_set['sat_or_not']
    z3_declare_set = result_set['declare_set']
    unknown_reason = result_set['unknown_reason']

    width = 52

    f = open(solution_txt, 'w')

    
    if sat_or_not == 'sat':

        z3_declare_set = _classify_declare_set(z3_declare_set, len(link_obj_set))

        sorted_declare_set = _sort_declare_set(z3_declare_set)

        link_id = 0
        for declare in sorted_declare_set:
            src_node_id = link_obj_set[link_id].src_node
            dst_node_id = link_obj_set[link_id].dst_node

            divider_between_link_str = '=' * width
            f.write("%s\n" % divider_between_link_str)

            src_to_dst = '(%d, %d)' % (src_node_id, dst_node_id)
            f.write('omega and rho at link %s, link_id: %d\n' % (src_to_dst, link_id))

            
            _format_omega_set_and_rho_set(f, declare, width)

            f.write('\n')

            link_id += 1
    elif sat_or_not == 'unsat':
        f.write('unsat\n')
    elif sat_or_not == 'unknown':
        f.write('unknown\n')
        
        f.write('the reason for unknown result: %s\n' % unknown_reason)

    
    _write_time_used_to_txt(f, time_used_in_second)

    f.close()


def _main():
    return


if __name__ == '__main__':
    _main()
