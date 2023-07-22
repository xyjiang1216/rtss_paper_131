import time

from z3 import *


def _parse_z3_model(model):
    solution = []
    for declare in model.decls():
        name = declare.name()
        value = model[declare]
        solution.append({'name': name, 'value': value})
    return solution


def add_and_solve_constraints(constraint_set,
                              timeout=-1):
    start = 0
    end = 0
    s = Solver()
    if timeout > 0:
        s.set(timeout=timeout)

    for constraint in constraint_set:
        s.add(constraint)

    declare_set = []
    unknown_reason = ''

    start = time.time_ns()

    sat_or_not = s.check()
    if sat_or_not == sat:
        model = s.model()
        end = time.time_ns()
        print("end time: %f" % end)

        declare_set = _parse_z3_model(model)
    elif sat_or_not == unsat:

        end = time.time_ns()

    elif sat_or_not == unknown:
        end = time.time_ns()

        unknown_reason = s.reason_unknown()
        pass

    time_used_in_second = (end - start) / 1000000000

    print('time_used:')
    print(time_used_in_second)

    return {'time_used_in_second': time_used_in_second, 'sat_or_not': str(sat_or_not),
            'declare_set': declare_set, 'unknown_reason': unknown_reason}


def _main():
    return


if __name__ == '__main__':
    _main()
