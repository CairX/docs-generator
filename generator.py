import re


def generator():
    tags = ['@class', '@method', '@param', '@return']

    with open('test.js', 'r') as f:
        comments = re.findall(r'(\/\*\*.+?\*\/)', f.read(), re.DOTALL)

        for comment in comments:
            comment = cleanComment(comment)
            index = indexArray(comment, tags)
            parts = split(comment, index)

            print(comment)
            print(parts)


def cleanComment(comment):
    comment = re.sub(r'(\n.+\*\s+)', ' ', comment)
    comment = comment.replace('/**', '', 1)
    comment = comment.replace('*/', '')
    comment = comment.strip()

    return comment


def indexArray(s, subs):
    result = []

    for sub in subs:
        result.extend(indexString(s, sub))

    result.sort()
    return result


def indexString(s, sub):
    index = 0
    result = []

    while index < len(s):
        index = s.find(sub, index)
        if index == -1:
            break

        result.append(index)
        index += len(sub)

    result.sort()
    return result


def split(s, index):
    result = []
    start = 0

    for end in index:
        sub = s[start:end]

        if len(sub) > 0:
            result.append(sub)

        start = end

    result.append(s[start:])

    return result


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


if __name__ == '__main__':
    print('Generator')
    generator()
