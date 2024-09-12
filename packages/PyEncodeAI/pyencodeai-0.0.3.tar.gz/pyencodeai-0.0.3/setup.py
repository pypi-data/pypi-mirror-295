import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyEncodeAI",
    version="0.0.3",
    author="Rafal Urniaz",
    description="Here gonna be something special ...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urniaz/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)