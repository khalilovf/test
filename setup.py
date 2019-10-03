from setuptools import setup
from versions import dependencies

VERSION = '0.1'


def main():
    setup(
        name='test',
        version=VERSION,
        description='piano test project',
        author='khalilov',
        install_requires=dependencies
    )


if __name__ == '__main__':
    main()
