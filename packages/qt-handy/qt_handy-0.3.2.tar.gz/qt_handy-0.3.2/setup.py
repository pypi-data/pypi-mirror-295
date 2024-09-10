from pathlib import Path

from setuptools import setup, find_packages

HERE = Path(__file__).parent.absolute()
with (HERE / 'README.md').open('rt') as fh:
    LONG_DESCRIPTION = fh.read().strip()

REQUIREMENTS: dict = {
    'core': [
        'qtpy',
    ],
    'test': [
        'pytest',
        'pytest-qt',
        'pytest-cov',
        'pytest-randomly',
    ],
    'dev': [
    ],
    'doc': [
    ],
}

setup(
    name='qt-handy',
    version='0.3.2',
    author='Zsolt Kovari',
    author_email='zsolt@kovaridev.com',
    description='A collection of useful Qt utilities and event filters for PyQt/PySide',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/plotlyst/qt-handy',

    packages=find_packages(),
    python_requires='>=3.7, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    install_requires=REQUIREMENTS['core'],
    extras_require={
        **REQUIREMENTS,
        'dev': [req
                for extra in ['dev', 'test', 'doc']
                for req in REQUIREMENTS.get(extra, [])],
        # The 'all' extra is the union of all requirements.
        'all': [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
)
