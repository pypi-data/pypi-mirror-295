from setuptools import setup, find_packages

setup(
    name='FeatureRefiner',  
    version='1.0.2',  
    description='A no-code solution for performing data transformations like imputation, encoding, scaling, and feature creation, with an intuitive interface for interactive DataFrame manipulation and easy CSV export.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    author='Ambily Biju', 
    author_email='ambilybiju2408@gmail.com',  
    url='https://github.com/ambilynanjilath/FeatureRefiner',  
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pandas>=1.0.0",
        "scikit-learn>=0.22.0",
        "numpy",
        "scipy",
        "streamlit",
        "streamlit-aggrid",
        "setuptools"
    ],
    entry_points={
        'console_scripts': [
            'run-FeatureRefiner = FeatureRefiner.scripts.run_app:main',
        ],
    },

    python_requires='>=3.8',  
    classifiers=[
        'Development Status :: 5 - Production/Stable',  
        'Intended Audience :: Developers',  
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',  
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='data transformation, imputation, encoding, scaling, feature creation, machine learning, data preprocessing, pandas, scikit-learn, feature engineering, data science, Python ',  
    project_urls={
        'Documentation': 'https://github.com/ambilynanjilath/FeatureRefiner/blob/main/README.md',
        'Source': 'https://github.com/ambilynanjilath/FeatureRefiner',
        'Tracker': 'https://github.com/ambilynanjilath/FeatureRefiner/issues',
    },
)