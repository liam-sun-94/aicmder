from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()


project_name = 'aicmder'
libinfo_py = path.join(here, project_name, '__init__.py')
libinfo_content = open(libinfo_py, 'r').readlines()
version_line = [l.strip() for l in libinfo_content if l.startswith('__version__')][0]
exec(version_line)


setup(
    name=project_name,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description='a simple ai cmder',
    long_description='Wait for updated',

    # The project's main homepage.
    # url='https://github.com/',

    # Author details
    author='Faith',
    author_email='xianzixiang@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Message Queues',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),


    install_requires=[
        'pyzmq>=17.1.0',
        'GPUtil>=1.3.0',
        'torch',
        'onnx',
        'onnx_tf',
        'pickle5',
        'packaging'
    ],
    extras_require={
        'http': ['fastapi', 'flask-json', 'uvicorn']
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'epd_group_id': [
    #         'my_pot = epd_main.tools:pot',
    #         'my_pan = epd_main.tools:pan',
    #         'my_colander = epd_main.tools:colander',
    #     ],
    # },
    entry_points={
        'console_scripts': ['aicmder=aicmder.commands.utils:execute'],
    },
    keywords='AI Cmder',
)