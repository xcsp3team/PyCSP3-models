from pycsp3.problems.data.parsing import *

from collections import defaultdict

dct = defaultdict(list)

while not line().startswith("% Obj"):
    if line().startswith("var"):
        dom = numbers_in(line())[:2]
        l = line()[line().index(':') + 2:line().rindex(';')]
        key = l[:5] + ('X' if l[-1] == 'X' or l.startswith('expectedArrivalTimeX') else '')
        if key[:5] in ('binop', 'objec') and '=' in l:
            name = l[:l.index('=') - 1]
            ctr = l[l.index('(') + 1:l.rindex(')')].split(" + ")
        else:
            name = l
            ctr = None
        dct[key].append((name, dom, ctr))
    elif line().startswith("constraint"):
        l = line()[line().index(' ') + 1:line().rindex(';')]
        if '->' in l:
            l = l.translate({ord(c): None for c in '()->='})
            l = l.replace('  ', ' ')
            t = l.split(' ')
            if l[0].isdigit():
                t[0], t[1] = t[1], t[0]
            t[1] = int(t[1])
            t[3] = int(t[3]) - 1
            dct['cimp'].append(t)
        elif ' in' in l:
            name = l[:l.index(" in")]
            values = numbers_in(l[l.index("{") + 1:l.rindex("}")])
            dct['cin'].append((name, values))
        elif l.startswith("(not"):
            l = l[1:-1]
            t = l[l.index("(") + 1:l.rindex(")")].split(" < ")
            dct['cnot'].append(t)
        elif l.startswith("all_different"):
            t = l[l.index("[") + 1:l.rindex("]") - 1].split(", ")
            dct['cad'].append(t)
        else:
            assert l.startswith("element"), l
            l = l[l.index('(') + 1:l.rindex(')')]
            index = l[:l.index(",")]
            if index.endswith('+1'):
                index = index[:-2]
            value = l[l.rindex(',') + 1:]
            if value.isdigit():
                value = int(value)
            l = l[l.index('[') + 1:l.rindex(']')]
            t = l.replace(' ', '').split(",")
            t = [int(v) if v.isdigit() else v for v in t]
            dct['celt'].append((index, value, t))
    next_line()

# data['variables'] = OrderedDict([(key, value) for key, value in dct.items()])


for key, value in dct.items():
    data[key] = value

# print(dct)
