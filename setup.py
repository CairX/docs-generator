from setuptools import setup

setup(
    name='docs-generator',
    description='Create markdown documentation based on comments in JavaScript files.',
    keywords='generator documentation markdown javascript',
    version='0.1dev0',
    author='Thomas Cairns',
    url='https://github.com/CairX/docs-generator',

    packages=['docs_generator'],
    entry_points={
        'console_scripts': [
            'docs-generator=docs_generator:main',
        ]
    },

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Documentation',
    ]
)
