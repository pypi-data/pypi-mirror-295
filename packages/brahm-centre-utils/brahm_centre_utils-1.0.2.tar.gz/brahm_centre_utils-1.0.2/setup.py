from setuptools import setup, find_packages

setup(
    name='brahm_centre_utils',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],
    description='Brahm Centre internal utility functions',
    author='Nguyen An Khanh',
    author_email='ankhanh@brahmcentre.com',
    url='https://github.com/Brahm-Centre-SG/bc-utils-package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)