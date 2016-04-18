import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_git_brokenlink_track',
    version='0.1.1.dev1',

    packages=find_packages(),
    install_requires=['requests'],
    keywords='git bug tracking django broken link',
    include_package_data=True,
    license='MIT',  # example license
    description='Django app which automates the issue creation on Git for broken links.',
    long_description=README,
    url='https://github.com/tarunbehal/django-git-brokenlink-track',
    author='Tarun Behal',
    author_email='tarunbehal@hotmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Quality Assurance'
    ],
)