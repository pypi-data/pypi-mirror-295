import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "mongol-register-parser",
    version = "0.0.1",
    author = "author",
    author_email = "elmerganbaa@gmail.com",
    description = "mongol register parser",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ganbaaelmer/mongol-register-parser.git",
    project_urls = {
        "Bug Tracker": "package issues URL",
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