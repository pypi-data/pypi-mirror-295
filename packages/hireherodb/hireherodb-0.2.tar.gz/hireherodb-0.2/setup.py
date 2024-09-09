from setuptools import setup, find_packages

setup(
    name="hireherodb",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy==2.0.32",
        "pydantic==2.8.2"
        ],
    python_requires='>=3.12'
)