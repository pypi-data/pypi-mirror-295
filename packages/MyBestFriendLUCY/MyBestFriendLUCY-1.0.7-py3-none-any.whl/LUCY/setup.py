from setuptools import setup, find_packages

setup(
    name='ethereum_predictor',
    version='1.0.1',
    author='Isaiah J Peterson',
    author_email='isaiahjpeterson@gmail.com',
    description='Ethereum Price Prediction Tool',
    packages=find_packages(),  # Automatically finds your package
    include_package_data=True,  # Include non-Python files
    install_requires=[
        'ccxt',
        'pandas',
        'numpy',
        'tensorflow',
        'joblib',
        'pandas_ta',
    ],
    entry_points={
        'console_scripts': [
            'eth_predictor=eth_predictor.app:main',  # Correctly references the main function in app.py
        ],
    },
)
