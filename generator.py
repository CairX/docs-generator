import re


def generator():
    with open('test.js', 'r') as f:
        #within = False
        another = False
        info = ''

        for line in f:
            line = line.strip()

            if another:
                info += line + '\n'
                block(info)
                info = ''
                another = False

            if line.startswith('/**'):
                info += line + '\n'
                #within = True
                #print('something')

            elif line.endswith('*/'):
                info += line + '\n'
                #within = False
                another = True

            elif line.startswith('*'):
                #line = line[1:].strip()
                info += line + '\n'


def block(info):
    result = {}
    for line in info.split('\n'):
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


if __name__ == '__main__':
    print('Generator')
    generator()
