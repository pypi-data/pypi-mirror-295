from setuptools import setup, find_packages

setup(
    name='pqcomponents',
    version='1.0.3',
    description='A custom PyQt5 widgets package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='majunggil',
    author_email='majunggil.work@gmail.com',
    url='https://github.com/majunggil/PyQt5/tree/main/pqwidgets',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
