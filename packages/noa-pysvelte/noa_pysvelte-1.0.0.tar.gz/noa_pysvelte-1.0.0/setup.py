"""Setup"""
from setuptools import setup, find_packages

setup(
    name="noa-pysvelte",
    version="1.0.0",
    packages=find_packages(),
    license="LICENSE",
    description="A library for visualising and interpreting model activations within a Jupyter Notebook. Fork of https://github.com/anthropics/PySvelte",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Noa Nabeshima",
    author_email="noanabeshima@gmail.com",
    url="https://github.com/noanabeshima/PySvelte",
    install_requires=[
        'einops',
        'numpy',
        'torch',
        'datasets',
        'transformers',
        'tqdm',
        'pandas',
        'typeguard~=2.0'
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)