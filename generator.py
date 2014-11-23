import re


def generator():
    with open('test.js', 'r') as f:
        another = False
        lines = []

        # TODO: Maybe use a regex instead...
        for line in f:
            line = line.strip()

            if another:
                lines.append(line)
                block(lines)
                lines = []
                another = False

            if line.startswith('/**'):
                lines.append(line)

            elif line.endswith('*/'):
                lines.append(line)
                another = True

            elif line.startswith('*'):
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

    result = {}
    a = testy.find('@')
    result['description'] = testy[:a]
    testy = testy[a:]

    breaks = []
    for v in valid:
        breaks.extend(index(testy, v))

    breaks.sort()

    testa = testy
    for i in range(len(breaks)):
        if i == 0:
            line = testa[:breaks[i+1]]
        elif i == len(breaks) - 1:
            line = testa[breaks[i]:]
        else:
            line = testa[breaks[i]:breaks[i+1]]

        ws = line.find(' ')
        if ws > 0:
            key = line[:ws]
            value = line[ws:].strip()
            if key == '@param':
                if key in result.keys():
                    result[key].append(value)
                else:
                    result[key] = [value]
            else:
                result[key] = value

    print(result)


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
