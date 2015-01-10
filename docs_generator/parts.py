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


class Comment(object):

    def __init__(self, parts):
        self.bind = None
        self.params = []

        for part in parts:
            part = part.strip()

            if part.startswith('@bind'):
                self.bind = part.replace('@bind', '').strip()

            elif part.startswith('@method'):
                self.method = part.replace('@method', '').strip()

            elif part.startswith('@param'):
                self.params.append(Param(part.replace('@param', '').strip()))

            elif not part.startswith('@'):
                self.description = part.strip()

    def __str__(self):
        result = ''

        if hasattr(self, 'method'):
            result += '\n\n## ' + self.method

        if hasattr(self, 'description'):
            result += '\n' + self.description + '\n'

        for param in self.params:
            result += '\n* ' + str(param)

        return result


class Section(object):

    def __init__(self, name):
        self.name = name
        self.comments = []

    def __str__(self):
        result = '# ' + self.name

        for comment in self.comments:
            result += str(comment)

        return result

    def add(self, comment):
        self.comments.append(comment)
