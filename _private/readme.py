import sys
import os
import os.path
import re

def create_alternative_models(name, directory):
    alternatives = {}
    p = re.compile(name + ".*.py")
    for file in os.listdir(directory):
        if p.match(file) and file != name+".py" and file != name+"1.py":
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
            alternatives[file] = {"tags": tags, "constraints": constraints}
    return alternatives




if __name__ == '__main__':
    constraints_path = "http://pycsp.org/documentation/constraints/"
    directories = ["academic", "single", "realistic", "crafted", "recreational"]
    for thedir in directories:
        problems = sorted([ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ])

        for p in problems:
            dir = f"{thedir}/{p}"
            model = f"{p}.py" if os.path.isfile(f"{dir}/{p}.py") else f"{p}1.py"
            alternatives = create_alternative_models(p, dir)
            model = dir+"/"+model

            inputlines = open(model, "r").readlines()
            outputfile = open(f"{dir}/README.md", "w")
            outputfile.write(f"# Problem {p}\n")
            outputfile.write("\n")
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

            if(len(alternatives) > 0):
                outputfile.write("\n<br />\n\n## _Alternative Models_\n\n")
                for k in sorted(alternatives.keys()):
                    outputfile.write("#### " + k + "\n")
                    outputfile.write(" - constraints: ")
                    outputfile.write(", ".join([f"[{c}]({constraints_path}{c})" for c in alternatives[k]["constraints"]]))
                    outputfile.write("\n")
                    outputfile.write(" - tags: ")
                    outputfile.write(", ".join([tag for tag in alternatives[k]["tags"]]))
                    outputfile.write("\n")
            outputfile.close()

