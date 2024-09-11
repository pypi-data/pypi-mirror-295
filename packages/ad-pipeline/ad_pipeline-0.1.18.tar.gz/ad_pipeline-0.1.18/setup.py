from setuptools import find_packages, setup

setup(
    name='ad_pipeline',
    packages=find_packages(include=['ad_pipeline', 'ad_pipeline.*']),
    version='0.1.18',
    description='AD Pipeline Beta',
    author='technology@firestorm.capital.com',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.2.2'],
    test_suite='tests',
)