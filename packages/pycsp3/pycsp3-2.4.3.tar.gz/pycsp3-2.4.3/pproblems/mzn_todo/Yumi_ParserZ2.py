from pycsp3.problems.data.parsing import *

nAgents = 2


def values(l):
    ns = numbers_in(l)
    return list(range(ns[0], ns[1] + 1)) if ".." in l else numbers_in(l)


skip_empty_lines(or_prefixed_by="%")
data['durations'] = [numbers_in(line())] + [numbers_in(next_line()) for _ in range(nAgents - 1)]
next_line(repeat=1)
skip_empty_lines(or_prefixed_by="%")
data['tray_tasks'] = values(line())
data['camera_tasks'] = values(next_line())
data['output_taks'] = values(next_line())
next_line()
skip_empty_lines(or_prefixed_by="%")
data['empty_gripper_task'] = values(line())
next_line()
skip_empty_lines(or_prefixed_by="%")
data['grippers'] = [numbers_in(l) for l in next_lines(prefix_stop="|]")]
next_line()
skip_empty_lines(or_prefixed_by="%")
data['suctions'] = [numbers_in(l) for l in next_lines(prefix_stop="|]")]
next_line()
skip_empty_lines(or_prefixed_by="%")
data['fixtures'] = [numbers_in(l) for l in next_lines(prefix_stop="|]")]
next_line()
skip_empty_lines(or_prefixed_by="%")
data['nCups'] = number_in(line())
next_line(repeat=1)
data['left_times'] = [numbers_in(l) for l in next_lines(prefix_stop="|]")]
next_line(repeat=1)
data['right_times'] = [numbers_in(l) for l in next_lines(prefix_stop="|]")]
assert len(data['left_times']) == len(data['right_times'])
next_line()
skip_empty_lines(or_prefixed_by="%")
data['locations'] = numbers_in(line())
data['futures'] = numbers_in(next_line())
data['tray_locations'] = values(next_line())
data['camera_locations'] = values(next_line())
data['fixture_locations'] = values(next_line())
data['airgun_locations'] = values(next_line())
data['output_locations'] = values(next_line())
