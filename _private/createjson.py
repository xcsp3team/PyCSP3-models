import json
import re
import os

models = []
directories = ["academic", "single", "realistic", "crafted", "recreational"]
#directories = ["recreational"]


def create_alternative_models(name, directory):
    alternatives = {}
    p = re.compile(name + ".*.py")
    for file in os.listdir(directory):
        if p.match(file) and file != name+".py":
            lines = open(f"{directory}/{file}", "r").readlines()
            start = False
            tags = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("## Tags"):
                    start = True
                elif start:
                    tags = [t.strip().rstrip(",") for t in stripped.split(" ")]
                    start = False
                if "constraints:" in line:
                    constraints = line.strip().split(":")[1].split(",")
                    constraints = sorted([c.strip() for c in constraints])
            alternatives[file[0:-3]] = {"tags": tags, "constraints": constraints}
    return alternatives

for thedir in directories:
    problems = sorted([name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name))])

    for p in problems:
        dir = f"{thedir}/{p}"
        model = f"{p}.py" if os.path.isfile(f"{dir}/{p}.py") else f"{p}1.py"
        originalmodel = model
        model = dir + "/" + model
        type = "CSP"
        lines = open(model, "r").readlines()
        constraints = []
        tags = []
        links = []
        start = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("minimize(") or stripped.startswith("maximize("):
                type = "COP"
            if stripped.startswith("- http"):
                links.append(stripped.split("-")[1].strip())
            if stripped.startswith("constraints") or stripped.startswith("Constraints"):
                constraints = [c.strip() for c in stripped.split(":")[1].split(',')]
            if stripped.startswith("## Tags"):
                start = True
            elif start:
                tags = [t.strip().rstrip(",") for t in stripped.split(" ")]
                start = False
        alternatives = create_alternative_models(p, dir)
        if not (originalmodel == f"{p}1.py" and len(alternatives) > 1):
            models.append(
                {"name": p, "fullname": dir, "constraints": constraints, "type": type, "tags": tags,
                 "links": links})

        for k in sorted(alternatives.keys()):
            models.append(
            {"name": k, "fullname": dir, "constraints": alternatives[k]['constraints'], "type": type, "tags": alternatives[k]['tags'],
             "links": links})

models.sort(key=lambda model: model["name"])
print(json.dumps(models))
