from setuptools import setup, find_packages

setup(
    name='easy_regression',
    version='0.1.0',
    py_modules=['easy_regression'],
    install_requires=[
        'openpyxl',  # Specify the dependency
    ],
    author='Deepan Kumar S',
    author_email='deepankumar2602@gmail.com',
    description='A tool for running and analyzing regression tests',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DeepanCoder/easy_regression',
    packages=find_packages(),
    package_data={
        'easy_regression': ['deepan_regression_tool.cpython-39-x86_64-linux-gnu.so'],  # Include the .so file in the package
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
