from pathlib import Path

from setuptools import find_packages, setup

#package meta-data
NAME = 'house_price_models_noom'
DESCRIPTION = "End-to-End house price prediction regression models"
URL = "https://github.com/Khannooman/HousePrice.git"
EMAIL = "khannooman8586@gmail.com"
AUTHOR = "Nooman"
REQUIRES_PYTHON = ">=3.6.0"

long_description = DESCRIPTION

# load the package's VERSION file as a dictionery
about = {}
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
PACKAGE_DIR = ROOT_DIR / 'regression_model'
with open(PACKAGE_DIR / "VERSION") as f:
    _version = f.read().strip()
    about["__version__"] = _version


# what pachage required for this module to be excutes?

def list_requests(filename="requirements.txt"):
    with open(f"{REQUIREMENTS_DIR}/{filename}") as fd:
        return fd.read().splitlines()
    

# Where the magic happens

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    package_data={"regression_model": ["VERSION"]},
    install_requires=list_requests(),
    extras_require={},
    include_package_data=True,
    license="BSD-3",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)


