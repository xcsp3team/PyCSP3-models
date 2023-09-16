import json
import sys
class _Options:
    def __init__(self):
        self.values = tuple()  # options with non-Boolean values (strings or numbers)
        self.flags = tuple()  # Boolean options
        self.parameters = []
        self.parameters_cursor = 0


    def set_values(self, *values):
        self.values = [value.lower() for value in values]
        for option in self.values:
            vars(self)[option] = None


    def set_flags(self, *flags):
        self.flags = [flag.lower() for flag in flags]
        for option in self.flags:
            vars(self)[option] = False


    def get(self, name):
        return vars(self)[name]


    def consume_parameter(self):
        if self.parameters_cursor < len(self.parameters):
            parameter = self.parameters[self.parameters_cursor]
            self.parameters_cursor += 1
            return parameter
        else:
            return None


    def parse(self, args):
        for arg in args:
            if arg[0] == '-':
                t = arg[1:].split('=', 1)
                t[0] = t[0].replace("-", "_")
                if len(t) == 1:
                    flag = t[0].lower()
                    if flag in self.flags:
                        vars(self)[flag] = True
                        assert flag not in self.values or flag == 'dataexport', "You have to specify a value for the option -" + flag
                    else:
                        print("Warning: the " + arg + " option is not an option.")
                else:
                    assert len(t) == 2
                    value = t[0].lower()
                    if value in self.values:
                        assert len(t[1]) > 0, "The value specified for the option -" + value + " is the empty string"
                        vars(self)[value] = t[1]
                    else:
                        print("Warning: the " + arg + " option is not an option.")
                        sys.exit(1)
            else:
                self.parameters.append(arg)



if __name__ == '__main__':
    Options = _Options()
    Options.set_values("constraint", "tag", "name")
    Options.set_flags("cop", "csp", "reverse", "json", "github", "help", "showtags", "showconstraints")
    Options.parse(sys.argv)

    if len(sys.argv) == 1 or (Options.csp and Options.cop) or (Options.json and Options.github):
        print("usage: python searchmodels.py [-constraint=Sum] [-tag=xcsp23] [-name='Bacp*'] [-cop|csp] [-reverse] [-json|-file] [-showtags] [-showcontraints]")
        sys.exit(1)
    if Options.help :
        print("usage: python searchmodels.py [-constraint=Sum] [-tag=xcsp23] [-name='Bacp'] [-cop|csp] [-reverse] [-json|-file] [-showtags] [-showcontraints]")
        print()
        print("Extract problems with respect to a given query. You can mix different queries resulting to all problems that matches all queries. You can also reverse the results.")
        print()
        print("  -help display this help and exit")
        print("  -showtags show all available tags")
        print("  -showconstraints show all available constraints")
        print()
        print("  -constraint=Sum  extract all problems with Sum constraint")
        print("  -tag=xcsp2  extract all problems with tag containing xcsp2 (xcsp22, xcsp23...)")
        print("  -name=Ba extract all problems containing BA as a substring")
        print("  -cop|-csp extract  cop or csp problems")
        print("  -reverse reverse the results")
        print()
        print("  -json display results as a json file")
        print("  -github display results as links to github project\n")
        sys.exit(1)
    results = []
    constraints = []
    problems = []
    tags = []
    csp = []
    cop = []
    models = json.load(open("_private/models.json"))
    if Options.showtags:
        tags = {}
        for model in models:
            for t in model['tags']:
                if t not in tags.keys():
                    tags[t] = 1
        print(" ".join(tags.keys()))
        sys.exit()

    if Options.showconstraints:
        constraints = {}
        for model in models:
            for c in model['constraints']:
                if c not in constraints.keys():
                    constraints[c] = 1
        print(" ".join(constraints.keys()))
        sys.exit()

    for model in models:
        if Options.constraint is not None:
            constraints.extend([model['name'] for c in model['constraints'] if c == Options.constraint])
        if Options.tag is not None:
            tags.extend([model['name'] for t in model['tags'] if Options.tag.upper() in t.upper()])
        if Options.name is not None and Options.name.upper() in model['name'].upper():
            problems.append(model['name'])
        if Options.csp and model['type'] == "CSP":
            csp.append(model['name'])
        if Options.cop and model['type'] == "COP":
            cop.append(model['name'])
    # Init results
    if Options.constraint is not None :
        results = constraints
    elif Options.name is not None :
        results = problems
    elif Options.tag is not None :
        results = tags
    elif Options.csp:
        results = csp
    elif Options.cop:
        results = cop


    # get intersction of filters
    if Options.constraint is not None :
        results = [r for r in results if r in constraints]
    if Options.name is not None :
        results = [r for r in results if r in problems]
    if Options.tag is not None :
        results = [r for r in results if r in tags]
    if Options.csp :
        results = [r for r in results if r in csp]
    if Options.cop :
        results = [r for r in results if r in cop]


    if Options.reverse :
        allmodels = [model['name'] for model in models]
        results = [m for m in allmodels if m not in results]

    if Options.json :
        tmp = [model for model in models if model['name'] in results]
        print(tmp)
    elif Options.github:
        for model in models:
            if model['name'] in results:
                print("https://github.com/xcsp3team/pycsp3-models//tree/main/" + model['fullname'])
    else:
        print(" ".join(results))