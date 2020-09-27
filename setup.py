
from setuptools import setup, find_packages

setup(
    name='oktaesri',
    version='1.0.1',
    packages=find_packages(include=['oktaesri']),
    url='http://faizantayyab.com',
    license='License.txt',
    author='FT',
    description='OKTA ESRI Integrator',
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.log', '*.in', '*.ini', '*.md']
    },
    setup_requires=[
        'requests~=2.24.0',
        'beautifulsoup4~=4.9.2'
    ],
    install_requires=[
        'requests~=2.24.0',
        'beautifulsoup4~=4.9.2'
    ]
)