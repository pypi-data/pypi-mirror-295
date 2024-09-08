from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Attention All you Need Transformer Model Page'
LONG_DESCRIPTION = 'A package that allows to build simple allow to use the Transformer model and some other helping package.'

# Setting up
setup(
    name="build_Transformer",
    version=VERSION,
    author="ProgramerSalar",
    author_email="<manishkumar60708090@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['torch'],
    keywords=['python', 'Transformer', 'LLM', 'build Transformer', 'chat-GPT Transformer', 'Meta Transformer'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)