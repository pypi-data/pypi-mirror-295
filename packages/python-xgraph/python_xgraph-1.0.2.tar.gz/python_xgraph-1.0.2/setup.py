# setup.py
from setuptools import setup, find_packages

setup(
    name="python-xgraph",
    version="1.0.2",
    author="Abhishek Sinha",
    author_email="sinha.abhishek.ai@gmail.com",
    description="A simple graph library with DFS, BFS, and cycle detection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sinha-abhishek-ai/python-xGraph",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
