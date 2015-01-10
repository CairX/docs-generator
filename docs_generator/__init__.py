from docs_generator import index
from docs_generator.parts import Section, Comment
import re
import sys


def main():
    print('Generator')
    generator(sys.argv[1:])


def generator(paths):
    tags = ['@bind', '@method', '@param', '@return', '@section']
    sections = {}

    for path in paths:
        try:
            with open(path, 'r') as f:
                comments = re.findall(r'(\/\*\*.+?\*\/)', f.read(), re.DOTALL)

                for comment in comments:
                    comment = cleanComment(comment)
                    positions = index.array(comment, tags)
                    parts = index.split(comment, positions)

                    title = getSectionTitle(parts)

                    if title:
                        sections[title] = Section(title)
                    else:
                        comment = Comment(parts)
                        sections[comment.bind].add(comment)

            print('Documentation done:', path)
        except FileNotFoundError:
            print('File not found:', path)

    with open('documentation.md', 'w') as f:
        for section in sections:
            f.writelines(str(sections[section]) + '\n\n')


def cleanComment(comment):
    comment = re.sub(r'(\n.+\*\s+)', ' ', comment)
    comment = comment.replace('/**', '', 1)
    comment = comment.replace('*/', '')
    comment = comment.strip()

    return comment


def getSectionTitle(parts):
    section = None

    for part in parts:
        part = part.strip()

        if part.startswith('@section'):
            section = part.replace('@section', '').strip()
            break

    return section
