import index
import re


class Param(object):

    def __init__(self, s):
        match = re.match(r'(\w+) \{(\w+?)\} (.+)', s)

        if match:
            self.name = match.group(1)
            self.type = match.group(2)
            self.description = match.group(3)

    def __str__(self):
        result = '**' + self.name + '**'
        result += ' *' + self.type + '*'
        result += ' ' + self.description

        return result


class Section(object):

    def __init__(self, parts):
        self.params = []

        for part in parts:
            part = part.strip()

            if part.startswith('@class'):
                self.clazz = part.replace('@class', '').strip()

            elif part.startswith('@method'):
                self.method = part.replace('@method', '').strip()

            elif part.startswith('@param'):
                self.params.append(Param(part.replace('@param', '').strip()))

            elif not part.startswith('@'):
                self.description = part.strip()

    def __str__(self):
        result = ''
        if hasattr(self, 'clazz'):
            result += '# ' + self.clazz + '\n'

        if hasattr(self, 'method'):
            result += '## ' + self.method + '\n'

        if hasattr(self, 'description'):
            result += self.description + '\n\n'

        for param in self.params:
            result += '* ' + str(param) + '\n'

        return result


def generator():
    tags = ['@class', '@method', '@param', '@return']

    with open('test.js', 'r') as f:
        comments = re.findall(r'(\/\*\*.+?\*\/)', f.read(), re.DOTALL)

        for comment in comments:
            comment = cleanComment(comment)
            positions = index.array(comment, tags)
            parts = index.split(comment, positions)

            print(Section(parts))


def cleanComment(comment):
    comment = re.sub(r'(\n.+\*\s+)', ' ', comment)
    comment = comment.replace('/**', '', 1)
    comment = comment.replace('*/', '')
    comment = comment.strip()

    return comment


if __name__ == '__main__':
    print('Generator')
    generator()
