from setuptools import setup, find_packages

setup(
    name='title_detection',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'xgboost',
        'pandas',
        'scikit-learn',
    ],
    description='Package for title detection using Neural Networks and XGBoost',
    author='Andrew Clayman',
    include_package_data=True,
)
