import os

from setuptools import PEP420PackageFinder, setup

setup(
    name='just-simulate',
    version=os.getenv('artifact_version', '0.0.0-dev'),
    description='just simulate',
    url='https://github.je-labs.com/BI-MachineLearning/just-simulate',
    author='Diego Peteiro',
    author_email='diego.peteiro@just-eat.com',
    license='Proprietary',
    packages=PEP420PackageFinder.find('src'),
    package_dir={'': 'src'},
    python_requires='>=3.7',
    zip_safe=False,
    install_requires=[
        'google-cloud-bigquery',
        'marshmallow',
        'numpy',
        'ortools',
        'pandas',
        'scipy'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ]
)
