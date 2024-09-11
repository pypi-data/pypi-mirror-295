from setuptools import setup, find_packages


with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name='table_data_process_lib',
    version='0.1.2',
    description='Library for table data processing',
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PavelMalyshev01/table_data_process_lib',
    author='Pavel Malyshev',
    author_email='p.malyshev@razumai.pro',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pandas',
        'xgboost',
        'scikit-learn',
        'imblearn'
    ],
    extras_requre={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    },
    python_requires='>=3.6',
)
