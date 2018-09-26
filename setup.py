import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

setup(
    name='pwngeth',
    version='0.0.1',
    author='maxzzze',
    description='Exploit misconfigured geth clients',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/maxzzze/pwngeth',
    zip_safe=False,
    packages=find_packages('pwngeth'),
    install_requires=[
    'web3',
    'Elasticsearch',
    'py-dateutil',
    'pytz',
    'shodan',
    'configargparse',
    'pyyaml'
    ],
    entry_points={
        'console_scripts':[
            'generate-targets-pg=pwngeth.console:generate_targets',
            'pwn-targets-pg=pwngeth.console:pwn_targets'
            ]
    }
)
