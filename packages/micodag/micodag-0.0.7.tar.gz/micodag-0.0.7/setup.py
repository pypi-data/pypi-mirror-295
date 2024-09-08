from setuptools import setup, find_packages
import os
VERSION = '0.0.7'
DESCRIPTION = 'A Python package of mixed integer convex programming for directed acyclic graphs.'


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()
# Setting up
setup(
    name="micodag",
    version=VERSION,
    author="Tong Xu",
    author_email="tongxu2027@u.northwestern.edu",
    description=DESCRIPTION,
    license="MIT",
    readme="README.md",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['gurobipy>=10.0.0', 'scipy>=1.11.1', 'cvxpy>=1.3.2', 'networkx>=3.0', 'numpy>=1.25.0'],
    python_requires=">=3.9",
    keywords=['python', 'Bayesian network'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
