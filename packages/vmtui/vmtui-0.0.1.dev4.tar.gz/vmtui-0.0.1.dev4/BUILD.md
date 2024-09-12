# BUILD Instructions

The package is uploaded to `PyPI` and available via `pip`.
It uses `setuptools` for the build process.

~~~bash
# install necessary packages for building and upload
pip install build twine
# build
python -m build
# upload to PyPI
twine upload --verbose dist/*
~~~