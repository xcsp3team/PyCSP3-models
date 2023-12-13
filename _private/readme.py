import sys
import os
import os.path

if __name__ == '__main__':
    constraints_path = "http://pycsp.org/documentation/constraints/"
    directories = ["academic", "single", "realistic", "crafted", "recreational"]

    for thedir in directories:
        problems = sorted([ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ])

        for p in problems:
            dir = f"{thedir}/{p}"
            model = f"{p}.py" if os.path.isfile(f"{dir}/{p}.py") else f"{p}1.py"
            model = dir+"/"+model
            print(model)

            inputlines = open(model, "r").readlines()
            outputfile = open(f"{dir}/README.md", "w")
            outputfile.write(f"# Problem {p}\n")
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
                    constraints = sorted([c.strip() for c in constraints])
                    outputfile.write(", ".join([f"[{c}]({constraints_path}{c})" for c in constraints]))
                    outputfile.write("\n")
                else:
                    if line.strip().startswith("python"):
                        if not python :
                            outputfile.write("```\n")
                            python = True
                    if not line.strip().startswith("python"):
                        if python:
                            outputfile.write("```\n")
                            python = False
                    outputfile.write(line)
            outputfile.close()