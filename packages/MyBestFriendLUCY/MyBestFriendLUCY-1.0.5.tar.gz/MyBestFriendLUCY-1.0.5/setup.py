from setuptools import setup, find_packages

setup(
    name="MyBestFriendLUCY",
    version="1.0.5",
    author="Isaiah",
    author_email="isaiahjpeterson007@gmail.com",
    description="Ethereum Price Prediction Package for Short-Term Trading",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/LUCY-1986-2009-project-ethereum-market-prediction-unit-limit_uncertainty,control_yourself--OurFriendLucy",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tensorflow>=2.0",
        "pandas",
        "ccxt",
        "pandas-ta",
        "numpy",
        "joblib",
        "scikit-learn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    # Add entry_points to make a command-line tool
    entry_points={
        'console_scripts': [
            'hey lucy=LUCY.app:main',  # Entry point for your command-line tool
        ],
    },
)
