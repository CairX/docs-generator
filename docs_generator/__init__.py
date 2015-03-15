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
    start = config.get('start', '/*').strip('"')
    end = config.get('end', '*/').strip('"')

    pattern = re.escape(start)
    pattern += '\n[\s\S]*?'
    pattern += re.escape(end)
    pattern += '\n.*?'
    print(pattern)

    tags = ['@bind', '@method', '@param', '@return', '@section']
    sections = []

    for path in paths:
        try:
            with open(path, 'r') as f:
                comments = re.findall(pattern, f.read())
                print(comments)

                for comment in comments:
                    comment = clean_comment(comment, start, end)
                    print(comment)
                    positions = index.array(comment, tags)
                    parts = index.split(comment, positions)

                    title = get_section_title(parts)

                    if title:
                        sections.append(Section(title))
                        print(title)
                    else:
                        try:
                            comment = Comment(parts)
                            sections[-1].add(comment)
                        except:
                            print('Missing section.')

            print('Documentation done:', path)
        except FileNotFoundError:
            print('File not found:', path)

    with open('documentation.md', 'w') as f:
        for section in sections:
            f.writelines(str(section) + '\n\n')


def clean_comment(comment, start, end):
    comment = comment.replace(start, '')
    comment = comment.replace(end, '')
    comment = re.sub(r'(\n.+\*\s+)', ' ', comment)
    comment = comment.strip()

    return comment


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
