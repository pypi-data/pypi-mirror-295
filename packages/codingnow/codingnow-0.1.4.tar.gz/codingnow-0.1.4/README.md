# codingnow_py
# CodingNow

CodingNow

pip install setuptools wheel twine

# build
python setup.py sdist bdist_wheel

# upload
twine upload dist/*
twine upload --verbose dist/*

# update
pip install codingnow --upgrade

#24.09.11
add background
add level control