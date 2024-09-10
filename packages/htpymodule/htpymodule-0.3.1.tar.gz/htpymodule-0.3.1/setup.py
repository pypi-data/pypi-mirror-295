from setuptools import setup, find_packages

setup(
    name="htpymodule",
    version="0.3.1",
    packages=find_packages(),
    description="A very simple example module for basic arithmetic operations.",
    long_description=open('README.md').read(),  # Read the content of your README file for a long description
    long_description_content_type='text/markdown',  # Ensure the long description is in markdown format
    author="Jason Dsouza, ChatGPT, and Hongtao Hao",
    author_email="hhao9@wisc.edu",
    # your source code url:
    url="https://github.com/hongtaoh/htpymodule/",
    install_requires=[
        # add any additional packages that 
        # needs to be installed along with your package. Eg: 'pandas'
    ],
)
