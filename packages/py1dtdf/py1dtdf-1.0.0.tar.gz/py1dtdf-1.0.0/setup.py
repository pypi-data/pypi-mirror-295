from setuptools import setup, find_packages

setup(
    name="py1dtdf",
    version="1.0.0",
    description="A comprehensive package for extracting standard, fractal, and complexity-based time-domain features from 1-D signals.",
    author="Rakshit Mittal",
    author_email="pypi@rakshitmittal.net",
    url="https://gitlab.rakshitmittal.net/rmittal/py1dtdf",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "nolds"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
