from docs_generator import index
from docs_generator.parts import Section
import re
import sys


def generator(paths):
    tags = ['@class', '@method', '@param', '@return']
    documentation = ''

    for path in paths:
        try:
            with open(path, 'r') as f:
                comments = re.findall(r'(\/\*\*.+?\*\/)', f.read(), re.DOTALL)

                for comment in comments:
                    comment = cleanComment(comment)
                    positions = index.array(comment, tags)
                    parts = index.split(comment, positions)

                    documentation += str(Section(parts)) + '\n\n'

            print('Documentation done:', path)
        except FileNotFoundError:
            print('File not found:', path)

    with open('documentation.md', 'w') as f:
        f.write(documentation)


def cleanComment(comment):
    comment = re.sub(r'(\n.+\*\s+)', ' ', comment)
    comment = comment.replace('/**', '', 1)
    comment = comment.replace('*/', '')
    comment = comment.strip()

    return comment


def main():
    print('Generator')
    generator(sys.argv[1:])
