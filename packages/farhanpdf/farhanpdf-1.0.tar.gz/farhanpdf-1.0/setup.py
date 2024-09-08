import setuptools
from pathlib import Path

setuptools.setup(
    name="farhanpdf",
    version=1.0,
    long_description=Path("README.md").read_text(encoding='utf-8'),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
