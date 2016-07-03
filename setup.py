import os

import setuptools

from bublik import VERSION

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setuptools.setup(
    name='django-bulk-update',
    version=VERSION,
    author='Shakurov Vadim Vladimirovich',
    author_email='apelsinsd@gmail.com',
    url='https://github.com/newvadim/hydra',
    long_description=README,
    description='Bulk update given objects using minmal query over Django ORM.',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
