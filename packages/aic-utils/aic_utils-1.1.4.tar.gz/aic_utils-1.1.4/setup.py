# setup.py

from setuptools import setup, find_packages

setup(
    name='aic_utils',
    version='1.1.4',
    packages=find_packages(),
    install_requires=[
        'google-cloud-storage',
        'slack_sdk'
        # Add other dependencies here
    ],
    author='Dylan D',
    author_email='dylan.doyle@jdpa.com',
    description='AIC API wrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dylandoyle11/aic_utils', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


