from pycsp3.problems.data.parsing import *

program_setup_time = number_in(line())
sequence_setup_time = number_in(next_line())
data['setup_times'] = OrderedDict([("program", program_setup_time), ("sequence", sequence_setup_time)])
data['max_colors_per_job'] = number_in(next_line())
min_cycles_per_job = number_in(next_line())
max_cycles_per_job = number_in(next_line())
data['cycles_per_job'] = OrderedDict([("min", min_cycles_per_job), ("max", max_cycles_per_job)])
data['max_jobs'] = number_in(next_line())
# nColors = data['nColors'] = number_in(next_line())
nColors = number_in(next_line())
nPrograms = number_in(next_line())
nMoulds = number_in(next_line())
nDemands = number_in(next_line())
data['nLines'] = number_in(next_line())
number_in(next_line())  # data['reference_makespan']
number_in(next_line())  # data['reference_tardiness'] =
number_in(next_line())  # data['reference_waste'] =
available_moulds = numbers_in_lines_until(";")
slots_programs = numbers_in(next_line())
cycle_time_programs = numbers_in(next_line())
program_moulds = numbers_in_lines_until(";")
line_moulds = numbers_in_lines_until(";")
t = numbers_in_lines_until(";")[1:]  # because 2 of 2d
data['color_compatibility'] = split_with_rows_of_size(t, nColors)
qty = numbers_in_lines_until(";")
due = numbers_in_lines_until(";")
cd = numbers_in_lines_until(";")
md = numbers_in_lines_until(";")

data["programs"] = [OrderedDict([("slots", slots_programs[i]), ("cycle_time", cycle_time_programs[i])]) for i in range(nPrograms)]
data["moulds"] = [OrderedDict([("available", available_moulds[i]), ("program", program_moulds[i]), ("line", line_moulds[i])]) for i in range(nMoulds)]
data["demands"] = [OrderedDict([("quantity", qty[i]), ("due", due[i]), ("color", cd[i]), ("mould", md[i])]) for i in range(nDemands)]
