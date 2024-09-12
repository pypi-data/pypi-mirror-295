from setuptools import find_packages, setup

with open("readme.md", "r") as file:
    long_description = file.read()

setup(
    name="websockethost",
    version="0.1.3",
    description="Web and python socket host",
    package={"": ""},
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamalice20/websockethost",
    author="lamalice20",
    author_email="discord974a@gmail.com",
    install_requires=[""],
    python_requires=">=3.12.5",
)