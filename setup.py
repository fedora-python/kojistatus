from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = ''.join(f.readlines())

NAME = 'kojistatus'

setup(
    name=NAME,
    version='0.2',
    description='Fetches the last statuses of Fedora Koji builds',
    long_description=long_description,
    author='Miro Hrončok',
    author_email='miro@hroncok.cz',
    keywords='koji fedora status',
    license='MIT',
    url='https://github.com/hroncok/' + NAME,
    install_requires=['requests', 'Flask'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3', 'betamax', 'pytest-flake8'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
