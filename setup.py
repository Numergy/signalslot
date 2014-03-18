import os.path

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='signalslot',
    version='0.0.1',
    description='Simple Signal/Slot implementation',
    url='https://github.com/numergy/signalslot',
    long_description=read('README.rst'),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    keywords='signal slot',
    install_requires=[
        'six',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

