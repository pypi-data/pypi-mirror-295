from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.0'
DESCRIPTION = 'likhil'
LONG_DESCRIPTION = 'A package to print your name on the screen'

# Setting up
setup(
    name="likhil",
    version=VERSION,
    author="Tadinada Likhil Venkata Naga Sri Sai Vimal",
    author_email="likhilpnl@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license='MIT',
    packages=find_packages(),
    install_requires=[''],
    keywords=['pattern', 'turtle', 'name','nameprint', 'python tutorial', 'Tadinada likhil venkata naga sri sai vimal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)