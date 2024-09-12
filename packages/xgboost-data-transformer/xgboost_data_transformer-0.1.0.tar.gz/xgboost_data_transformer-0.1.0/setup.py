# setup.py
from setuptools import setup, find_packages

setup(
    name='xgboost_data_transformer',
    version='0.1.0',
    description='A package for transforming raw data for XGBoost.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Noorain Kazmi',
    author_email='noosykaz@gmail.com',
    url='https://github.com/noorains/xgboost_data_transformer',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
