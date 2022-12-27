import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coordsystems",
    version="0.0.1",
    author="Heliton Martins",
    author_email="helitonmrf@gmail.com",
    description="A package for dealing with different coordinate reference system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hellmrf/coordsystems",
    packages=["coordsystems"],
    package_dir={"coordsystems": "src"},
    install_requires=[
        'numpy>=1.20.1',
        'plum-dispatch'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
