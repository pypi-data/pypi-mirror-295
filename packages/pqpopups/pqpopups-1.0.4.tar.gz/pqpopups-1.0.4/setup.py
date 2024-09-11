from setuptools import setup, find_packages

setup(
    name='pqpopups',
    version='1.0.4',
    description='A custom PyQt5 popups package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='kwonyoungil',
    author_email='kwen232@gmail.com',
    url='https://github.com/kyi1107/pqpopups',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
        'pqwidgets>=1.0.7',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
