from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="tc-hivemind-backend",
    version="1.4.4.post1",
    author="Mohammad Amin Dadgar, TogetherCrew",
    maintainer="Mohammad Amin Dadgar",
    maintainer_email="dadgaramin96@gmail.com",
    packages=find_packages(),
    description="This repository is a shared library for together hivemind etl and bot codes.",
    long_description=open("README.md").read(),
    install_requires=requirements,
)
