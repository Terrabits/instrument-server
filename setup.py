from setuptools import find_packages, setup

setup(
    name='instrument-server',
    version='1.0.0',
    description='TCP server for controlling multiple instruments with a simplified SCPI interface',
    long_description=open('README.md').read().strip(),
    author='Nick Lalic',
    author_email='nick.lalic@gmail.com',
    url='http://path-to-my-packagename',
    py_modules=['instrument_server'],
    packages=find_packages(exclude=['test']),
    install_requires=['ruamel.yaml>=0.15.85<1.0', 'pyvisa>=1.9.1<2.0'],
    extras_require={
    'dev':  ['ddt>=1.2.0<2.0'],
    'test': ['ddt>=1.2.0<2.0']
    },
    license='MIT License',
    zip_safe=False,
    keywords='RF instrument SCPI',
    classifiers=['Packages', 'RF'],
    entry_points={
    'console_scripts': [
        'instrument-server=instrument_server.bin.instrument_server:main'
    ]
    })
