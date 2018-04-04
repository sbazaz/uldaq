from setuptools import setup


def read_contents(file_to_read):
    with open(file_to_read, 'r') as f:
        return f.read()


setup(
    name='uldaq',
    version='0.1',
    description='Universal Library Python API for Measurement Computing DAQ devices',
    long_description=read_contents('README.md'),
    author='MCC',
    author_email="'techsupport@mccdaq.com",
    keywords=['uldaq', 'mcc', 'ul', 'daq'],
    license='MIT',
    include_package_data=True,
    packages=['uldaq'],
    install_requires=[
        'enum34;python_version<"3.4"',
    ],
)