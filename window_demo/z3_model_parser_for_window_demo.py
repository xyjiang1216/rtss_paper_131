from z3 import *
import re


def _classify_declare_set(declare_set, total_link_num):
    tmp_declare_set = [{'phi_array': {'name': '', 'value': ''},
                        'tau_array': {'name': '', 'value': ''},
                        'kappa_array': {'name': '', 'value': ''},
                        'omega_set': []}
                       for i in range(total_link_num)]

    
    
    
    
    
    for declare in declare_set:
        name = declare['name']
        value = declare['value']
        
        link_id = int(name.split('(')[1].split(')')[0])
        if re.match(r'P\^.', name):
            tmp_declare_set[link_id]['phi_array'] = declare
        elif re.match(r'T\^.', name):
            tmp_declare_set[link_id]['tau_array'] = declare
        elif re.match(r'K\^.', name):
            tmp_declare_set[link_id]['kappa_array'] = declare
        elif re.match(r'O_.', name):
            tmp_declare_set[link_id]['omega_set'].append(declare)
    
    return tmp_declare_set





def _transform_z3_array_to_list(array, gcl_len, omega_set):
    
    
    omega_set = [omega['value'] for omega in omega_set]
    
    array_to_list = ['n/a'] * gcl_len
    for i in range(gcl_len):
        if str(i) in omega_set:
            value = str(simplify(array[i]))
            array_to_list[i] = value
    return array_to_list




def _transform_z3_declare_set_to_readable_declare_set(declare_set,
                                                      link_obj_set):
    link_id = 0
    for declare in declare_set:
        omega_set = declare['omega_set']
        gcl_len = link_obj_set[link_id].gcl_len

        
        
        
        if not omega_set:
            for array_name in ['phi_array', 'tau_array', 'kappa_array']:
                declare[array_name]['value'] = ['n/a'] * gcl_len
        
        elif omega_set:
            for array_name in ['phi_array', 'tau_array', 'kappa_array']:
                array = declare[array_name]['value']
                array_to_list = _transform_z3_array_to_list(array, gcl_len, omega_set)
                declare[array_name]['value'] = array_to_list
            declare['omega_set'] = _sort_z3_int_ref(omega_set)
        link_id += 1
    
    return declare_set



def _sort_z3_int_ref(omega_set):
    
    for omega in omega_set:
        omega['value'] = str(omega['value'])
    
    omega_set.sort(key=lambda x: x['value'])
    return omega_set



def _format_table_header_or_array(fd, name, array, width):
    
    length = len(array)
    format_list = ['|', name, '|']
    for item in array:
        format_list.append(str(item))
        format_list.append('|')

    format_str = "{0[0]}{0[1]:^%d}{0[2]}" % width
    index = 3
    for i in range(length):
        format_str = format_str + "{0[%d]:^%d}{0[%d]}" % (index, width, index + 1)
        index += 2

    fd.write(format_str.format(format_list))
    fd.write('\n')

    divider = '|' + '-' * width + '|'
    for i in range(length):
        divider = divider + '-' * width + '|'

    fd.write(divider)
    fd.write('\n')



def _write_arrays_to_txt(fd, phi_array, tau_array, kappa_array, width):
    
    table_len = len(phi_array['value'])
    name = 'INDEX'
    value = range(table_len)
    _format_table_header_or_array(fd, name, value, width)
    
    
    name = 'phi'
    value = phi_array['value']
    _format_table_header_or_array(fd, name, value, width)
    
    name = 'tau'
    value = tau_array['value']
    _format_table_header_or_array(fd, name, value, width)
    
    name = 'kappa'
    value = kappa_array['value']
    _format_table_header_or_array(fd, name, value, width)



def _write_omega_to_txt(f, omega_set, gcl_len, width):
    width = width + 6
    f.write('stream\'s window index as follow:\n')
    divider_between_array_and_int_str = '-' * (3 * (width+1) + 1)
    f.write("%s\n" % divider_between_array_and_int_str)

    
    format_str = '{}{:^%d}{}{:^%d}{}{:^%d}{}' % (width, width, width)
    f.write(format_str.format('|', 'stream_id', '|', 'instance_id', '|', 'omega', '|'))
    f.write('\n')
    f.write(format_str.format('|', '-' * width, '|', '-' * width, '|', '-' * width, '|'))
    f.write('\n')

    for omega in omega_set:
        name = omega['name']
        
        value = omega['value']
        
        
        stream_id = name.split('_')[1].split(',')[0]
        instance_id = name.split(',')[1].split('^')[0]
        f.write(format_str.format('|', stream_id, '|', instance_id, '|', value, '|'))
        f.write('\n')
        f.write(format_str.format('|', '-' * width, '|', '-' * width, '|', '-' * width, '|'))
        f.write('\n')

    f.write("%s\n" % divider_between_array_and_int_str)


def _write_time_used_to_txt(f, time_used_in_second):
    divider = '+' * 80
    f.write('%s\n' % divider)
    f.write('time used:\n')
    f.write("%s s\n" % time_used_in_second)
    f.write("%s min\n" % (time_used_in_second / 60))
    return



def write_declare_set_to_txt(result_set,
                             link_obj_set,
                             solution_txt):
    time_used_in_second = result_set['time_used_in_second']
    sat_or_not = result_set['sat_or_not']
    z3_declare_set = result_set['declare_set']
    unknown_reason = result_set['unknown_reason']

    f = open(solution_txt, 'w')

    
    if sat_or_not == 'sat':
        width = 9

        z3_declare_set = _classify_declare_set(z3_declare_set, len(link_obj_set))

        readable_declare_set = _transform_z3_declare_set_to_readable_declare_set(z3_declare_set, link_obj_set)

        link_id = 0
        for declare in readable_declare_set:
            gcl_len = link_obj_set[link_id].gcl_len
            src_node_id = link_obj_set[link_id].src_node
            dst_node_id = link_obj_set[link_id].dst_node

            divider_between_link_str = '=' * ((gcl_len+1) * (width+1) + 1)
            f.write("%s\n" % divider_between_link_str)

            src_to_dst = '(%d, %d)' % (src_node_id, dst_node_id)
            f.write('arrays at link %s, link_id: %d\n' % (src_to_dst, link_id))

            
            _write_arrays_to_txt(f,
                                 declare['phi_array'],
                                 declare['tau_array'],
                                 declare['kappa_array'],
                                 width)

            
            omega_set = declare['omega_set']
            _write_omega_to_txt(f, omega_set, gcl_len, width)

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
