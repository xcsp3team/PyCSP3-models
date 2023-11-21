import json
import os

import os

models = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py") and "PARSER" not in file.upper() and file not in ["createjson.py", "readme.py", "searchmodels.py"]:
            model = os.path.join(root, file)[2:]
            type = "CSP"
            name = os.path.basename(model).split(".")[0]
            f = open(model, "r")
            lines = f.readlines()
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
                    constraints = [c.strip() for c in stripped.split(":")[0].split(',')]
                if stripped.startswith("## Tags"):
                    start = True
                elif start:
                    tags = [t.strip().rstrip(",") for t in stripped.split(" ")]
                    start = False
            f.close()
            models.append({"name": name, "fullname": os.path.dirname(model), "constraints" : constraints, "type": type, "tags": tags, "links": links})

models.sort(key=lambda model: model["name"])
print(json.dumps(models))

