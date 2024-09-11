from pycsp3.problems.data.parsing import *


def read_series(sets=False):
    t = []
    while not next_line()[-1] == ';':
        t.append(numbers_in(line()) if sets is False else read_sets(line()))
    return t


def read_sets(l):
    l = l.replace(" ", "")
    return [numbers_in(tok) for tok in l[l.index('{') + 1:l.rindex('}')].split('},{')]


skip_empty_lines(or_prefixed_by="%")

data['durations'] = [numbers_in(line()), numbers_in(next_line())]
next_line()
data['nTrayTasks'] = n = numbers_in(next_line())[1]
data['cameraTasks'] = numbers_in(next_line())
data['outputTasks'] = numbers_in(next_line())
data['empty_gripper_tasks'] = numbers_in(next_line())
data['gripper_pick_tasks_orders'] = read_series()
data['suction_pick_tasks_orders'] = read_series()
data['fixture_task_orders'] = read_series()

next_line()
skip_empty_lines(or_prefixed_by="%")
data['no_suction_cups'] = number_in(line())
next_line()
data['left_arm_travel_times'] = read_series()
next_line()
data['right_arm_travel_times'] = read_series()
next_line()
skip_empty_lines(or_prefixed_by="%")
data['location_order'] = numbers_in(line())
data['FixtureWorkObstruction'] = numbers_in(next_line())
data['TRAY_LOCATIONS'] = numbers_in(next_line())
data['CAMERA_LOCATIONS'] = numbers_in(next_line())
data['FIXTURE_LOCATIONS'] = numbers_in(next_line())
data['AIRGUN_LOCATIONS'] = numbers_in(next_line())
data['OUTPUT_LOCATIONS'] = numbers_in(next_line())
next_line()
skip_empty_lines(or_prefixed_by="%")
data['wait_zones_left_data'] = read_sets(line())
data['wait_zones_right_data'] = read_sets(next_line())
data['work_zones_left_data'] = read_sets(next_line())
data['work_zones_right_data'] = read_sets(next_line())
next_line()
data['travel_zones_left_data'] = read_series(True)
next_line()
data['travel_zones_right_data'] = read_series(True)
