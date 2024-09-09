from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="cv_timeseries",
    version="0.0.2",
    author="Ana",
    author_email="sofia.mirandaalbuquerque@gmail.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anasofiama/package_creation.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)