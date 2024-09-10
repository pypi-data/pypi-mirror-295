from setuptools import setup, find_packages

setup(
    name='PreproX',  # Your package name
    version='0.1.0',
    description='A Python library for data preprocessing suggestions and transformations',
    author='Samama Farooq',
    author_email='samama4200@gmail.com',
    url='https://github.com/Sam-Coding77/DataWiz',  # Optional, replace with your repo URL
    packages=find_packages(),  # Automatically find all packages in your project
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'category-encoders',
        'psutil',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
