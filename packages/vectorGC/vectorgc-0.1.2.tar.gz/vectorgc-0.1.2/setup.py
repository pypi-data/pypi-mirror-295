from setuptools import setup, find_packages

setup(
    name='vectorGC',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        "rdkit>=2023.3.3",
        "numpy>=1.26.0",
        "pandas>=2.0.3",
        "torch>=2.1.0",
        "feos>=0.4.3",
        "feos_torch>=0.1.0",
        "scipy>=1.11.4",
        "tqdm>=4.66.1"
    ],
    author='Carl Hemprich',
    author_email='chemprich@ethz.ch',
    description='Implementation of the Vector-GC method and its regression framework',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'  
    ],
)

