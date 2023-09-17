import sys
import os

if __name__ == '__main__':
    constraints_path = "http://pycsp.org/documentation/constraints/"

    model = sys.argv[1]
    name = os.path.basename(model).split(".")[0]
    dir = os.path.dirname(model)
    inputlines = open(model, "r").readlines()
    outputfile = open(f"{dir}/README.md", "w")
    outputfile.write(f"# Problem {name}\n")
    outputfile.write("## Description\n")
    start = False
    python = False
    for line in inputlines:
        if line == '"""\n':
            if start:
                break
            start = True
            continue
        if "constraints:" in line:
            outputfile.write("  constraints: ")
            constraints = line.strip().split(":")[1].split(",")
            constraints = [c.strip() for c in constraints]
            outputfile.write(", ".join([f"[{c}]({constraints_path}{c})" for c in constraints]))
            outputfile.write("\n")
        else:
            if line.startswith("python"):
                if not python :
                    outputfile.write("```\n")
                    python = True
            if not line.startswith("python"):
                if python:
                    outputfile.write("```\n")
                    python = False
            outputfile.write(line)
    outputfile.close()