from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="metalmental_logger",
    version="0.6",
    author="MetalMental",
    author_email="flupino@metalmental.net",
    license="MIT",
    url="https://github.com/Flupinochan/MetalMentalPythonLogger",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
