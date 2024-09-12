 
from setuptools import setup, find_packages

setup(
    name="pydaffodil",
    version="1.0.0",
    description="A reusable deployment framework for Python.",
    author="Mark Wayne Menorca",
    author_email="marcuwynu23@gmail.com",
    packages=find_packages(),
    install_requires=[
        "paramiko",
        "tqdm",
        "colorama"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
