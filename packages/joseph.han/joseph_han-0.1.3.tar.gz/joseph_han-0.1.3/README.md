# codingnow_py
# CodingNow

CodingNow

pip install setuptools wheel twine

# build
python setup.py sdist bdist_wheel

# upload
twine upload dist/*
twine upload --verbose dist/*