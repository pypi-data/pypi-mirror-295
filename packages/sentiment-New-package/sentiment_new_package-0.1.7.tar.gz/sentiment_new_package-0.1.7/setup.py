from setuptools import setup, find_packages

setup(
    name='sentiment_New_package',
    version='0.1.7',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'sentiment_analysis': ['sentiment_model.pkl', 'vectorizer.pkl']
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
