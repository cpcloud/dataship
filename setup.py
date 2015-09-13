import os
from setuptools import setup, find_packages

import versioneer


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='dataship',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Phillip Cloud',
    author_email='cpcloud@gmail.com',
    description='Relationships for your data',
    license='BSD',
    keywords='data database',
    packages=find_packages(),
    install_requires=read('requirements.txt').strip().split('\n'),
    long_description=read('README.rst'),
    zip_safe=False,
    entry_points={
        'console_scripts': ['shipit = dataship.relate.shipit']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
    ],
)
