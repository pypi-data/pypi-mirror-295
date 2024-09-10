from setuptools import setup, find_packages

setup(
    name='codingnow',
    version='0.1.0',
    author='Your Name',
    author_email='codingnow@naver.com',
    description='A simple example Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cflab2017/codingnow_py',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)