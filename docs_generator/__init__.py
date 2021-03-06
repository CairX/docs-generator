from docs_generator import index
from docs_generator.parts import Section, Comment
from configparser import ConfigParser
import re
import sys


"""
    TODO
        - Add ignore option for part of method name in config ex. this or self.
"""


def main():
    print('Generator')
    config = ConfigParser()
    config.read('documentation.conf')

    if config.sections():
        generator(sys.argv[1:], config['comments'])
    else:
        print('Missing config file: documentation.conf')


def generator(paths, config):
    start = config.get('start', '/*').strip('"')
    between = config.get('between', '*').strip('"')
    end = config.get('end', '*/').strip('"')
    ignore = config.get('ignore', '')

    pattern = re.escape(start)
    pattern += '\n[\s\S]*?'
    pattern += re.escape(end)
    pattern += '\n^.*$'

    tags = ['@bind', '@method', '@param', '@return', '@section']
    sections = []

    for path in paths:
        try:
            with open(path, 'r') as f:
                comments = re.findall(pattern, f.read(), re.MULTILINE)

                for comment in comments:
                    comment, extra_line = clean_comment(comment, start, between, end)
                    extra_line = extra_line.replace(ignore, '')
                    positions = index.array(comment, tags)
                    parts = index.split(comment, positions)

                    title = get_section_title(parts)

                    if title:
                        sections.append(Section(title, parts))
                    else:
                        comment = Comment(parts, extra_line)
                        try:

                            sections[-1].add(comment)
                        except:
                            print('Missing section.')

            print('Documentation done:', path)
        except FileNotFoundError:
            print('File not found:', path)

    with open('documentation.md', 'w') as f:
        for section in sections:
            f.writelines(str(section) + '\n\n')


def clean_comment(comment, start, between, end):
    extra_line_position = comment.rfind(end) + len(end)
    extra_line = comment[extra_line_position:]
    comment = comment[:extra_line_position]

    comment = comment.replace(start, '')
    comment = comment.replace(end, '')
    pattern = '(\s*' + re.escape(between) + '\s*)'
    comment = re.sub(pattern, ' ', comment)
    comment = comment.strip()

    return comment, extra_line


def get_section_title(parts):
    section = None

    for part in parts:
        part = part.strip()

        if part.startswith('@section'):
            section = part.replace('@section', '').strip()
            break

    return section


def get_level(string):
    return ((len(string) - len(string.lstrip(' '))) / 4)
