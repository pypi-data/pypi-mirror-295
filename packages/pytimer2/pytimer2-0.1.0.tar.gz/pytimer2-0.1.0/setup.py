# setup.py

from setuptools import setup, find_packages

setup(
    name="pytimer2",
    version="0.1.0",
    author="Atiqur Rahman",
    author_email="rahman.md.attiq@gmail.com",
    description="PyTimer is a lightweight and easy-to-use Python package designed to provide countdown timer functionality. It offers a simple class-based approach to manage countdowns, making it perfect for various use cases such as timing events, tracking intervals, or managing delays in scripts and applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/attiqRahman/pytimer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)