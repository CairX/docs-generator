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

    valid = ['@class', '@method', '@param', '@return']

    for v in valid:
        breaks = index(testy, v)

    breaks.sort()

    restult = {}
    result['description'] = testy[:breaks[0]]
    breaks = breaks[1:]

    #for index in breaks:
    #    ws =

    print(testy)

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

    while index < len(s):
        index = s.find(sub, index)
        if index == -1:
            break

        print(index)
        index += len(sub)


if __name__ == '__main__':
    print('Generator')
    generator()
