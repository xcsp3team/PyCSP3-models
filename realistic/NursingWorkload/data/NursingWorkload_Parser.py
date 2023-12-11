""""
Parser for WagInstances at Problem 040 on CSPLib
"""
from pycsp3.problems.data.parsing import *

nZones, nNurses = t = numbers_in(line())
lbPatient, ubPatient, limit = numbers_in(next_line())
demands = [numbers_in(next_line())[1:] for _ in range(nZones)]

data['nNurses'] = nNurses
data['minPatientsPerNurse'] = lbPatient
data['maxPatientsPerNurse'] = ubPatient
data['maxWorkloadPerNurse'] = limit
data['demands'] = demands
