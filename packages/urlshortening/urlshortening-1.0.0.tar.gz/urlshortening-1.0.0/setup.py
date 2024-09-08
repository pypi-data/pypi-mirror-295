import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="urlshortening",
    version="1.0.0",
    url='https://github.com/Enkompass/django-urlshortening',
    license='BSD',
    description="A URL shortening app for Django.",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Enkompass',
    author_email='jvazquez@enkompass.net',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['setuptools', 'six', 'Django>=3.2,<6.0'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
