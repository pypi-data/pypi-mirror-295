from setuptools import setup, find_packages

setup(
    name='pqutils',
    version='1.0.9',
    description='A utils package for PyQt5',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='majunggil',
    author_email='majunggil.work@gmail.com',
    url='https://github.com/majunggil/PyQt5/tree/main/pqutils',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
