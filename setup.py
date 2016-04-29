from setuptools import setup, find_packages

setup(
    name='egpackager',
    version='0.0.1',
    url='https://github.com/VUEG/egpackager',
    license='MIT',
    author='Joona Lehtomäki',
    author_email='joona.lehtomaki@gmail.com',
    description='Simple Python CLI tool for creating data packages',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Data management',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['data']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "gspread>=0.3.0",
        "click>=6.6"
    ],

    entry_points={'console_scripts': [
        'egpackager = egpackager.cli:cli'
        ]
    }
)
