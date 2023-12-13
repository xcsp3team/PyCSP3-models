import json
import os

import os

models = []
directories = ["academic", "single", "realistic", "crafted", "recreational"]

for thedir in directories:
    problems = sorted([name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name))])

    for p in problems:
        dir = f"{thedir}/{p}"
        model = f"{p}.py" if os.path.isfile(f"{dir}/{p}.py") else f"{p}1.py"
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
        models.append(
            {"name": p, "fullname": model, "constraints": constraints, "type": type, "tags": tags,
             "links": links})

models.sort(key=lambda model: model["name"])
print(json.dumps(models))
