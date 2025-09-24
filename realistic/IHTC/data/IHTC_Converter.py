import json

from pycsp3.problems.data.parsing import *

with open(options.data) as f:  # options.data is the name of the JSON file whose format must be converted
    d = json.load(f)

data["nDays"] = d.get("days")
data["nSkills"] = d.get("skill_levels")
data["shift_types"] = d.get("shift_types")
data["age_groups"] = d.get("age_groups")
data["occupants"] = d.get("occupants")

patients = d.get("patients")
for i, patient in enumerate(patients):
    if not "surgery_due_day" in patient:
        its = list(patient.items())
        its.insert(1 + next(i for i, t in enumerate(its) if t[0] == "surgery_release_day"), ("surgery_due_day", 100_000))
        patients[i] = {k: v for k, v in its}
data["patients"] = patients
data["surgeons"] = d.get("surgeons")
data["theaters"] = d.get("operating_theaters")
data["rooms"] = d.get("rooms")
data["nurses"] = d.get("nurses")
data["weights"] = d.get("weights")
