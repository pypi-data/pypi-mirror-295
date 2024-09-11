import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "mongol_register_parser",
    version = "0.0.5",
    author = "Ganbaatar Bold",
    author_email = "elmerganbaa@gmail.com",
    description = "mongol register parser",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ganbaaelmer/mongol_register_parser.git",
    project_urls = {
        "Bug Tracker": "https://github.com/ganbaaelmer/mongol_register_parser.git",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)