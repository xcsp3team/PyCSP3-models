import json
import sys

import os

models = []
for root, dirs, files in os.walk("."):
    if "./_private" in root:
        continue
    for file in files:
        if file.endswith(".py") and "parser" not in file:
            model = os.path.join(root, file)[2:]
            type = "CSP" if "CSP" in model else "COP"
            f = open(model, "r")
            lines = f.readlines()
            constraints = ""
            for line in lines:
                if "constraints:" in line or "Constraints" in line:
                    constraints = line
            f.close()
            name = os.path.basename(model).split(".")[0]
            models.append({"name": name, "fullname": model[:-3], "constraints" : constraints, "type": type})

print(models)
