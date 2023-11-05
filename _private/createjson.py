import json
import os

import os

models = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py") and "PARSER" not in file.upper() and file not in ["createjson.py", "readme.py", "searchmodels.py"]:
            model = os.path.join(root, file)[2:]
            type = "CSP" if "CSP" in model else "COP"
            name = os.path.basename(model).split(".")[0]
            f = open(model, "r")
            lines = f.readlines()
            constraints = []
            tags = []
            start = False
            for line in lines:
                if line.startswith("constraints") or line.startswith("Constraints"):
                    constraints = [c.strip() for c in line.strip().split(":")[1].split(',')]
                if line.startswith("## Tags"):
                    start = True
                elif start:
                    tags = [t.strip().rstrip(",") for t in line.strip().split(" ")]
                    start = False
            f.close()
            models.append({"name": name, "fullname": os.path.dirname(model), "constraints" : constraints, "type": type, "tags": tags})

models.sort(key=lambda model: model["name"])
print(json.dumps(models))

