from setuptools import setup, find_packages

setup(
    name='numpy2ometiff',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tifffile'
    ],
    author='Tristan Whitmarsh',
    author_email='tw401@cam.ac.uk',
    description='A Python library to write NumPy arrays to OME-TIFF format.',
    license='BSD 3-Clause License',
    keywords='OME TIFF NumPy microscopy',
)