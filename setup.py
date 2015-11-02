from beout import __version__
from setuptools import find_packages, setup

setup(
    name='beout',
    version=__version__,
    description='beout  is a library for easily generating beautiful output for long-running processes',
    author='Zoltan Nagy',
    author_email='zoltan.nagy@prezi.com',
    url='https://github.com/abesto/beout',
    packages=find_packages(),
    license='MIT',
    keywords='terminal',
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['humanize', 'termcolor']
)
