from setuptools import setup, find_packages

setup_requires=['setuptools_scm'],

setup(
    name='atlast',
    version='0.1',
    author='Thomas Moore',
    author_email='tmoore11@qub.ac.uk',
    description='cleaning ATLAS photometry',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'numpy',
    ],
)
