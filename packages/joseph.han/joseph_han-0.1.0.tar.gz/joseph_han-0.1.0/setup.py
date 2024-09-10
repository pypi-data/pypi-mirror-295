from setuptools import setup, find_packages

setup(
    name='joseph.han',
    version='0.1.0',
    author='codingnow',
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