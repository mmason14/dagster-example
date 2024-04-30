from setuptools import find_packages, setup

setup(
    name="the_project",
    packages=find_packages(exclude=["the_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "PyGithub",
        "matplotlib",
        "pandas",
        "nbconvert",
        "nbformat",
        "ipykernel",
        "jupytext",
        "pyspark",
        "pydexcom",
        "dagster_aws"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
