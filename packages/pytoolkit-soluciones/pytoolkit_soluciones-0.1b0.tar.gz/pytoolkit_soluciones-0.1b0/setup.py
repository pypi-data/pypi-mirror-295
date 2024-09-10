# setup.py

from setuptools import setup, find_packages

setup(
    name="pytoolkit_soluciones",
    version="0.1-beta",
    packages=find_packages(),
    install_requires=[],
    author="Cristian Pavez",
    author_email="cpavezm@soluciones.cl",
    description="",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
