from setuptools import setup

# For release: `python -m pip install build && python -m build .`
# The upload both the sdist and wheel under ./dist

setup(
    name='ccl-flatten-json',
    packages=['flatten_json'],
    version='0.2.1',
    description='Flatten JSON objects',
    license='MIT',
    author='C-Change Labs Inc.',
    author_email='support@c-change-labs.com',
    url='https://github.com/cchangelabs/ccl-flatten-json',
    keywords=['json', 'flatten', 'pandas'],
    classifiers=[],
    entry_points={
        'console_scripts': ['flatten_json=flatten_json:cli']
    },
    install_requires=['six'],
)
