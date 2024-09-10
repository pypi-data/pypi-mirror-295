from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='send2trash3k',
    version='0.0.0.1',
    packages=['send2trash3k'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
    