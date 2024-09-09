from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='rahhscidow',  # Your package name
    version='1.1',
    description='A Scihub paper downloader.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Use 'text/markdown' if you're using Markdown
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[],  # Add your dependencies here
    # other setup parameters
)
