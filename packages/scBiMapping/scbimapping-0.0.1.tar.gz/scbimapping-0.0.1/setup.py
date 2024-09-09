import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scBiMapping", 
    version="0.0.1", 
    author="Teng Qiu",
    author_email="qiutengcool@163.com",
    description="scBiMapping is a tool for non-linear dimension reduction method suitable for large-scale high-dimensional sparse single-cell datasets such as scRNA, scATAC, scHi-C, etc, with very few runtime and memory cost.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={
        'scBiMapping': ['*.so'], 
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
