from setuptools import setup, find_packages

setup(
    name="fintechff_indicator",
    version="1.1.0",
    description="A python package for providing fintech indicators",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jonathan Lee",
    author_email="lihuapinghust@gmail.com",
    url="https://github.com/lihuapinghust/fintechff_indicator",
    packages=find_packages(),
    install_requires=[
        "backtrader",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
