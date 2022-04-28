from setuptools import find_packages, setup


description='A tool for creating Test and Measurement microservices'


setup(
    name='instrument-server',
    version='2.1.1',
    description=description,
    long_description=description,
    author='Nick Lalic',
    author_email='nick.lalic@gmail.com',
    url='https://github.com/Terrabits/instrument-server',
    py_modules=['instrument_server'],
    packages=find_packages(exclude=['tests']),
    install_requires=['ruamel.yaml>=0.15.85<1.0', 'pyvisa>=1.9.1<2.0'],
    extras_require={
        'dev':  ['ddt>=1.2.0<2.0', 'twine>=3.8.0', 'wheel>=0.37.1'],
        'dist': ['twine>=3.8.0', 'wheel>=0.37.1'],
        'test': ['ddt>=1.2.0<2.0']
    },
    license='R&S Terms and Conditions for Royalty-Free Products',
    zip_safe=False,
    keywords='RF instrument SCPI',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Environment
        'Environment :: Console',

        # OS
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',

        # Rohde & Schwarz Royalty-Free products license
        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
    'console_scripts': [
        'instrument-server=instrument_server.bin.instrument_server:main'
    ]
    })
