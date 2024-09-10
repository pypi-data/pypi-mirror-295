from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pydota2',
    version='0.0.0.1',
    packages=['pydota2'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
    