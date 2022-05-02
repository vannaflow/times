from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="times",
    version="0.0.1",
    author="Kyle Horne",
    author_email="me@kyhorne.com",
    description="A set of financial utility functions for analyzing dates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vannaflow/times",
    project_urls={
        "Bug Tracker": "https://github.com/vannaflow/times/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
)
