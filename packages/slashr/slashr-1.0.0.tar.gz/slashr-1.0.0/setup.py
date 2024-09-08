from setuptools import setup

version = "1.0.0"
short = '\\r Never lose your cursor again!'
with open ('README.md', 'r') as f:
    long = f'{f.read()}\ngithub: https://github.com/JustRedTTG/slashr'

# Setting up
setup(
    name="slashr",
    version=version,
    author="Red",
    author_email="redtonehair@gmail.com",
    description=short,
    long_description_content_type="text/markdown",
    long_description=long,
    packages=['slashr'],
    install_requires=['colorama', 'cursor'],
    keywords=['python', 'terminal'],
)
