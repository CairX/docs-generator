import re


def generator():
    with open('test.js', 'r') as f:
        comments = re.findall(r'(\/\*\*.+?\*\/)', f.read(), re.DOTALL)

        for comment in comments:
            block(comment.split('\n'))

            clean = re.sub(r'(\n.+\*\s+)', ' ', comment)
            clean = clean.replace('/**', '', 1)
            clean = clean.replace('*/', '')
            clean = clean.strip()
            #print(clean)


def block(lines):
    testy = ''
    name = ''

    for line in lines:
        line = line.strip()
        if line.startswith('/**'):
            testy += line.replace('/**', '', 1).strip()
        elif line.endswith('*/'):
            testy += line[:-2]
        elif line.startswith('*'):
            testy += line.replace('*', '', 1).strip()
        else:
            name = line.strip()

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

    #result['name'] = name

    #print(result)
    out(result)


def out(o):
    result = ''

    if '@class' in o:
        result += '# ' + o['@class'] + '\n'

    if '@method' in o:
        result += '## ' + o['@method'] + '\n'

    if 'description' in o:
        result += o['description'] + '\n\n'

    if '@param' in o:
        for p in o['@param']:
            m = re.match(r'(\w+) \{(\w+?)\} (.+)', p)
            if m:
                #print(m.group())
                #print(m.group(1))
                #print(m.group(2))
                #print(m.group(3))
                result += '**' + m.group(1) + '**'
                result += ' *' + m.group(2) + '*'
                result += ' ' + m.group(3) + '\n\n'
            #result += p + '\n'

    #print('-----------------------')
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
