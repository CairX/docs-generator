from docs_generator import index
from docs_generator.parts import Section, Comment
from configparser import ConfigParser
import re
import sys


def main():
    print('Generator')
    config = ConfigParser()
    config.read('documentation.conf')
    generator(sys.argv[1:], config['comments'])


def generator(paths, config):
    pattern = re.escape(config.get('start', '/*').strip('"'))
    pattern += '(.+?)'
    pattern += re.escape(config.get('end', '*/').strip('"'))
    # print(pattern)

    tags = ['@bind', '@method', '@param', '@return', '@section']
    sections = {}

    for path in paths:
        try:
            with open(path, 'r') as f:
                comments = re.findall(pattern, f.read(), re.DOTALL)

                for comment in comments:
                    comment = cleanComment(comment)
                    positions = index.array(comment, tags)
                    parts = index.split(comment, positions)

                    title = getSectionTitle(parts)

                    if title:
                        sections[title] = Section(title)
                        print(title)
                    else:
                        try:
                            comment = Comment(parts)
                            sections[comment.bind].add(comment)
                        except KeyError:
                            print('Missing bind.')

            print('Documentation done:', path)
        except FileNotFoundError:
            print('File not found:', path)

    with open('documentation.md', 'w') as f:
        for section in sections:
            f.writelines(str(sections[section]) + '\n\n')


def cleanComment(comment):
    comment = re.sub(r'(\n.+\*\s+)', ' ', comment)
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
