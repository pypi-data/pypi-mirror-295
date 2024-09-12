from setuptools import setup, find_packages

setup(
    name="megaprofiler",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "numpy",
        "tabulate",
        "scikit-learn",
        "imbalanced-learn",
        "statsmodels",
        "scipy"
    ],
    entry_points={
        'console_scripts': [
            'megaprofiler=megaprofiler.cli:main',  
        ],
    },
    description=(
        "megaprofiler is a highly customizable and extensible data profiling library "
        "designed to help data scientists and engineers understand their datasets "
        "before performing analysis or building models."
    ),
    long_description=(
        "When working with large datasets, it’s often necessary to understand data types, "
        "distributions, and potential issues (e.g., missing values, outliers) before analysis. "
        "While libraries like pandas-profiling exist, there is still room for an extensible, easy-to-use, "
        "and highly customizable profiler that integrates data validation.\n\n"
        "Key Features:\n"
        "- **Automatic Data Summaries**: Provide insights like distribution, unique values, missing values, and more for each column.\n"
        "- **Anomaly Detection**: Automatically flag columns or rows with unusual distributions, outliers, or inconsistent data.\n"
        "- **Data Validation**: Set validation rules (e.g., no missing values in specific columns, data type constraints) and get alerts if the data violates these rules.\n"
        "- **Custom Reports**: Generate visual reports (e.g., HTML, PDF) with configurable thresholds for what counts as an anomaly.\n"
        "- **Data Drift Detection**: Track changes in data distributions over time to identify shifts in data quality or content.\n\n"
        "Benefits:\n"
        "megaprofiler would be invaluable to data scientists and engineers dealing with exploratory data analysis, "
        "data quality checks, and ETL pipelines, reducing manual data investigation and improving data quality oversight."
    ),
    long_description_content_type="text/markdown",
    author="Siddharth Krishnan",
    author_email="sid@sidkrishnan.com",
    url="https://github.com/sidkris/megaprofiler",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
