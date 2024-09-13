from setuptools import setup, find_packages

setup(
    name='title_detection',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'torch',
        'xgboost',
        'pandas',
        'numpy',
        'scikit-learn',
    ],
    author='Andrew Clayman',
    description='Title Detection using NN and XGBoost',

)
