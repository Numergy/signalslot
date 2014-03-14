from setuptools import setup, find_packages


setup(
    name='signalslot',
    version='0.0.1',
    description='Simple Signal/Slot implementation',
    url='https://github.com/numergy/signalslot',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
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

