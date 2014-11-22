import re


def generator():
    with open('test.js', 'r') as f:
        #within = False
        another = False
        lines = []

        for line in f:
            line = line.strip()

            if another:
                lines.append(line)
                block(lines)
                lines = []
                another = False

            if line.startswith('/**'):
                lines.append(line)
                #within = True
                #print('something')

            elif line.endswith('*/'):
                lines.append(line)
                #within = False
                another = True

            elif line.startswith('*'):
                #line = line[1:]s.strip()
                lines.append(line)


def block(lines):
    testy = ''
    for line in lines:
        if line.startswith('/**'):
            testy += line.replace('/**', '', 1).strip()
        elif line.endswith('*/'):
            testy += line[:-2]
        elif line.startswith('*'):
            testy += line.replace('*', '', 1).strip()

    #print(testy)

    valid = ['@class', '@method', '@param', '@return']

    result = {}
    a = testy.find('@')
    result['description'] = testy[:a]
    testy = testy[a:]

    breaks = []
    for v in valid:
        breaks.extend(index(testy, v))

    breaks.sort()

    #result['description'] = testy[:breaks[0]]
    #testy = testy[breaks[0]:]
    #breaks = breaks[1:]

    testa = testy
    for i in range(len(breaks)):
        if i == 0:
            line = testa[:breaks[i+1]]
        elif i == len(breaks) - 1:
            line = testa[breaks[i]:]
        else:
            line = testa[breaks[i]:breaks[i+1]]

        #print(line)

        ws = line.find(' ')
        if ws == -1:
            result[line] = ''
        else:
            result[line[:ws]] = line[ws:].strip()

    """
    test = testy
    for b in breaks:
        line = test[:b]
        test = test[b:]
        ws = line.find(' ')
        result[line[:ws]] = line[ws:]
    """
    print(result)

    """
    result = {}
    for line in lines:
        print(line)
        if (line.startswith('*/') or line.startswith('/**')):
            continue
        elif line.startswith('*'):
            line = line[1:].strip()
            if line.startswith('@'):
                try:
                    first = line.index(' ')
                except ValueError:
                    continue
                key = line[:first]
                value = line[first:]
                result[key] = value
            else:
                result['description'] = line
        else:
            p = re.compile('(function )(.+?)(\()')
            m = p.match(line)

            if m:
                result['name'] = m.group(2)
            else:
                p2 = re.compile('(var )(.+?)(= function)')
                m2 = p2.match(line)
                if m2:
                    result['name'] = m2.group(2)

    print(result)
    """


def index(s, sub):
    index = 0
    result = []

    while index < len(s):
        index = s.find(sub, index)
        if index == -1:
            break

        result.append(index)
        index += len(sub)

    return result


if __name__ == '__main__':
    print('Generator')
    generator()
