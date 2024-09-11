from setuptools import setup,find_packages

with open("README.md","r") as file:
    description=file.read()

setup(
    name="StefanTools",
    version="1.4",
    packages=find_packages(),
    install_requires=[
        "rich",
        "inputimeout",
        "inflect"
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)