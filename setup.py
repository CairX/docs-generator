from setuptools import setup

setup(
    name='docs-generator',
    version='0.1dev0',
    packages=['docs_generator'],
    entry_points={
        'console_scripts': [
            'docs-generator=docs_generator:main',
        ]
    }
)
