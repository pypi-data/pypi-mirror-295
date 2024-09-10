from setuptools import setup, find_packages
# use readme.md as long_description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="psgd_torch",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "torch",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)