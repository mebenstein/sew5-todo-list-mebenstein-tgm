import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Todo List",
    version="0.0.1",
    author="Michael Ebenstein",
    author_email="mebenstein@student.tgm.ac.at",
    description="Todo List 4 SEW",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
)