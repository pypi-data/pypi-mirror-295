from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as stream:
    long_description = stream.read()

setup(
    name="AsiacellX",
    author="ZOOM",
    version="1.0.0",
    description="A Python library for interacting with Asiacell's website and mobile application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['Python', 'Asiacell', 'API', 'Iraq', 'SMS validation'],
    python_requires='>=3.6',
)
