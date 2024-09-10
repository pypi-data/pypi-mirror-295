from setuptools import setup, find_packages

with open("README.MD", "r") as f:
    description = f.read()

setup(
    name="SWELib",
    version="2.1.1",
    packages=find_packages(),
    install_requires=[
        'numpy==1.23.5',
        'matplotlib==3.7.1'
    ],
    long_description=description,
    long_description_content_type='text/markdown',
)
