from setuptools import setup, find_packages

setup(
    name='dutch_flag',
    version='0.1.2',
    packages=find_packages(),
    description='A minimalistic python library solving the Dutch national flag problem.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sergei Shteiner',
    author_email='sergei.shteiner@gmail.com',
    url="https://github.com/sergei-shteiner/dutch_flag",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)