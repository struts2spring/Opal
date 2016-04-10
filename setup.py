__author__ = 'vijay'

from setuptools import setup

setup(
    name='Opal',
    version='0.1',
    url='https://github.com/struts2spring/Opal',
    license='BSD',
    author='Vijay',
    author_email='',
    description='Opal is a advance book management system.',
    long_description=__doc__,
    packages=['src', 'src.dao', 'src.logic','src.selenium_download','src.static', 'src.ui', 'src.ui.view','src.ui.view.opalview','src.ui.view.thumb','src.util'],
    py_modules=['opal'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'wxPython >=2.9.1.1',
        'SQLAlchemy >= 1.0.11',
        'selenium',
        'PyPDF2'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ]
      )