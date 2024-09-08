#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='pokerkit',
    version='0.5.4',
    description='An open-source Python library for poker game simulations, hand evaluations, and statistical analysis',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/uoftcprg/pokerkit',
    author='University of Toronto Computer Poker Student Research Group',
    author_email='uoftcprg@studentorg.utoronto.ca',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords=[
        'artificial-intelligence',
        'deep-learning',
        'game',
        'game-development',
        'game-theory',
        'holdem-poker',
        'imperfect-information-game',
        'libratus',
        'pluribus',
        'poker',
        'poker-engine',
        'poker-evaluator',
        'poker-game',
        'poker-hands',
        'poker-library',
        'poker-strategies',
        'python',
        'reinforcement-learning',
        'texas-holdem',
    ],
    project_urls={
        'Documentation': 'https://pokerkit.readthedocs.io/en/latest/',
        'Source': 'https://github.com/uoftcprg/pokerkit',
        'Tracker': 'https://github.com/uoftcprg/pokerkit/issues',
    },
    packages=find_packages(),
    python_requires='>=3.11',
    package_data={'pokerkit': ['py.typed']},
)
