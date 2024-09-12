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

#24.09.11 version='0.1.5'
add background
add level control

#24.09.12 version='0.1.6'
add draw mouse position
add effect for game-over

#24.09.12 version='0.1.7'
bug fix gameover