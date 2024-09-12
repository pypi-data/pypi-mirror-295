from setuptools import setup, find_packages
setup(
    name="minefob",
    version="1.0.2.1",
    packages=find_packages(include=["requests", "json", "time", "datetime"])
)