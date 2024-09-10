import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "bi-coopdevs-utils",
    version = "0.0.1",
    author = "Coopdevs",
    author_email = "info@coopdevs.org",
    description = "Util functions for BI",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6"
)
