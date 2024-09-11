from setuptools import setup, find_packages

setup(
    name='sentiment_New_package',
    version='0.1.1',
    description='A package for sentiment analysis using pre-trained models',
    author='Drish',
    author_email='udayveer.deswal@drishinfo.com',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'joblib',
        'nltk',
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)