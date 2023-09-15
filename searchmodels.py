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
    Options.set_flags("cop", "csp", "reverse")
    Options.parse(sys.argv)

    if len(sys.argv) == 1 or (Options.csp and Options.cop):
        print("usage: python searchmodels.py [-constraint=Sum] [-tag=xcsp23] [-name='Bacp*'] [-cop|csp] [-reverse]")
        sys.exit(1)
    results = []
    constraints = []
    problems = []
    tags = []
    csp = []
    cop = []
    models = json.load(open("_private/models.json"))
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
    print("results: ", results)
