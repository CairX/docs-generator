import index
import re


def generator():
    tags = ['@class', '@method', '@param', '@return']

    with open('test.js', 'r') as f:
        comments = re.findall(r'(\/\*\*.+?\*\/)', f.read(), re.DOTALL)

        for comment in comments:
            comment = cleanComment(comment)
            positions = index.array(comment, tags)
            parts = index.split(comment, positions)

            print(comment)
            print(parts)


def cleanComment(comment):
    comment = re.sub(r'(\n.+\*\s+)', ' ', comment)
    comment = comment.replace('/**', '', 1)
    comment = comment.replace('*/', '')
    comment = comment.strip()

    return comment


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
                result += '**' + m.group(1) + '**'
                result += ' *' + m.group(2) + '*'
                result += ' ' + m.group(3) + '\n\n'

    print(result)


if __name__ == '__main__':
    print('Generator')
    generator()
