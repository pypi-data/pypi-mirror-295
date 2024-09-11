import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

try:
    with open("version.txt", "r") as file:
        version = file.read().replace("\n", "")
except FileNotFoundError:
    version = "0.0.0"

setuptools.setup(
    name="cdisc-library-keyediffer",
    version=version,
    author="Geraud Campion",
    author_email="gcampion@cdisc.org",
    description="A library for diffing structured data, like json or xml files, where the two files being diffed share some common structure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cdisc-org/cdisc-library-keyediffer",
    packages=setuptools.find_packages(include=["keyediffer", "keyediffer.*", "keyediffer.resources"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "genson>=1.2.2",
        "jsonpath-ng>=1.5.2",
        "jsonschema>=3.2.0",
        "requests>=2.22.0",
        "xlsxwriter>=1.3.8",
    ],
    package_data={"": ["resources/*"]},
    include_package_data=True,
)
