DEBUG = 0
separator = {'{', '}', '(', ')', ',', '"', ' '}

def splitEachTokenRetardVersion(line):
    aux = line.split()
    for s in separator:
        aux2 = []
        if (DEBUG): print(aux, s)
        for a in aux:
            if (DEBUG): print(a, s)
            if (a == s):
                aux2 += [a]
                continue
            string = ""
            for c in a:
                if (c == s):
                    aux += [s]
                    if (string != ""): aux2 += [string]
                    string = ""
                else:
                    string += c
            if (string != ""): aux2 += [string]
        aux = aux2
    return(aux)

def splitEachToken(line):
    token = []
    newCol, string = 0, ""
    for col, c in enumerate(line):
        if (c in separator):
            if (string != ""): token += [[newCol, string]]
            if (c != ' '): token += [[col + (newCol != 0), c]]
            newCol, string = col + 2, ""
        else:
            string += c
    if (string != ""): token += [[newCol, string]]
    return(token)

lines = []
while (True):
    try:
        lines += [input()]
    except EOFError as e:
        break

token = []
for l, line in enumerate(lines):
    line = splitEachToken(line)
    for t in line:
        token += [[l, t[0], t[1]]]

prev = 0
for t in token:
    if (t[0] > prev):
        prev = t[0]
        print()
    print("[%04d, %04d] () {%s}" % (t[0], t[1], t[2]))
