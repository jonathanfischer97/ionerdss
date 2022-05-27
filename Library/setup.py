from setuptools import find_packages, setup
setup(
    name='platonics',
    packages=find_packages(include=['platonics']),
    version='0.1.0',
    description='Functions to build dodecahedron',
    author='Zixiu Hugh Liu',
    license='Gnu PL 3.0',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
