from setuptools import setup, find_packages

setup(
    name='sentiment_New_package',
    version='0.1.6',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'sentiment_analysis': ['classifier.pkl', 'model_word.pkl']
    },
    install_requires=[
        'scikit-learn',
        'joblib',
        'numpy',
        'nltk'
    ],
    description='A package for sentiment analysis using pre-trained models',
    author='Drish',
    author_email='udayveer.deswal@drishinfo.com',
)
