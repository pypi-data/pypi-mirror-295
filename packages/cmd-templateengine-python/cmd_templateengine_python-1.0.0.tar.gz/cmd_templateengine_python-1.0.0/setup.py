"""
Sample template engine in Python
----------------------

Links
`````

* `development version <https://bitbucket.org/entinco/eic-templates-services-python/src/master/cmd-templateengine-python>`

"""

from setuptools import find_packages
from setuptools import setup

try:
    readme = open('readme.md').read()
except:
    readme = __doc__


setup(
    name='cmd-templateengine-python',
    version='1.0.0',
    url='https://bitbucket.org/entinco/eic-templateengine/src/master/cmd-templateengine-python',
    license='Commercial',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='Template Engine V1 - Create software component skeletons from templates',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
