from setuptools import setup, find_packages

setup(
    name='pii_scanner',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    tests_require=['unittest'],
    description='A library for scanning Personally Identifiable Information (PII).',
)
