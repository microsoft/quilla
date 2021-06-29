from setuptools import setup, find_packages


with open('VERSION') as f:
    version = f.read().strip()

with open('README.md') as f:
    long_description = f.read()

extra_dependencies = {
    'tests': [
        'flake8',
        'mypy',
        'pytest',
        'pytest-cov',
        'pytest-sugar',  # Added for better outputs
        'pytest-xdist',  # Parallelize the tests
    ],
    'docs': [
        'sphinx',
        'sphinx-rtd-theme',
        'sphinx_autodoc_typehints',
        'myst_parser',
        'sphinx_argparse_cli',
    ],
    'pytest': [  # For the plugin
        'pytest'
    ],
    'dev': [
        'pre-commit',
        'types-setuptools',  # Adds typing stubs
    ],
    'release': [
        'wheel',
        'twine',
        'gitchangelog',
        'pystache',
    ]
}

all_dependencies = []

for _, dependencies in extra_dependencies.items():
    all_dependencies.extend(dependencies)

all_dependencies = list(set(all_dependencies))  # Convert to set to remove overlaps
extra_dependencies['all'] = all_dependencies

setup(
    name='quilla',
    version=version,
    description='Declarative UI testing with JSON',
    author='Natalia Maximo',
    author_email='tal.afp.max@gmail.com',
    maintainer='CRE Avengers',
    maintainer_email='cre-avengers@microsoft.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/microsoft/quilla',
    python_requires='>=3.8',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'quilla': ['py.typed']
    },
    include_package_data=True,
    install_requires=[
        'selenium',
        'pluggy',
        'msedge-selenium-tools',
        'pydeepmerge'
    ],
    tests_require=extra_dependencies['tests'],
    extras_require=extra_dependencies,
    entry_points={
        'console_scripts': ['quilla = quilla:run'],
        'pytest11': [
            'quilla = pytest_quilla'
        ]
    },
    project_urls={
        'Issues': 'https://github.com/microsoft/quilla/issues',
        'Discussions': 'https://github.com/microsoft/quilla/discussions'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Typing :: Typed',
    ]
)
