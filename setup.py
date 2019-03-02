import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Commit Monitor",
    version="0.0.1",
    author="mozola",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests',
                      'flask',
                      'bs4',
                      'flake8',
                      'sphinx',
                      'pytest>=3.4.0',
                      'pytest-cov>=2.5.1'])
