# BUILD Instructions

The package is uploaded to `PyPI` and available via `pip`.
It uses `setuptools` for the build process.

~~~bash
# install necessary packages for building and upload
pip install build twine
# set version
git tag 0.9.0
git push --tags
# build
python -m build
# check 
twine check dist/*
# upload to PyPI
twine upload --verbose dist/*
~~~