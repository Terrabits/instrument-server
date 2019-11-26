from setuptools import find_packages, setup

setup(
    name='instrument-server',
    version='1.3.1',
    description='TCP server for controlling multiple instruments with a simplified SCPI interface',
    long_description=open('README.md').read().strip(),
    author='Nick Lalic',
    author_email='nick.lalic@gmail.com',
    url='https://github.com/Terrabits/instrument-server',
    py_modules=['instrument_server'],
    packages=find_packages(exclude=['test']),
    install_requires=['ruamel.yaml>=0.15.85<1.0', 'pyvisa>=1.9.1<2.0'],
    extras_require={
    'dev':  ['ddt>=1.2.0<2.0'],
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

        # Pick your license as you wish (should match "license" above)
        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    entry_points={
    'console_scripts': [
        'instrument-server=instrument_server.bin.instrument_server:main'
    ]
    })
