# setup.py

from setuptools import setup, find_packages

setup(
    name="lqlpath",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],  # Add any dependencies if needed
    description="A package for searching log query language path ",
    author="Harish Lohiya",
    author_email="harishlohiya@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    #url="https://github.com/logiconapp/lqlpath/",  # Replace with your repository
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
