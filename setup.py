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
    packages=['src', 'src.dao', 'src.dao.online', 'src.logic', 'src.logic.online', 'src.ui.view.online.thumb', 
              'src.metadata', 'src.selenium_download', 'src.static', 'src.ui', 'src.util',
              'src.ui.view', 'src.ui.view.epub', 'src.ui.view.kivy', 'src.ui.view.metadata', 'src.ui.view.metadata.review',
              'src.ui.view.online', 'src.ui.view.opalview', 'src.images', 'src.ui.view.thumb'],
    py_modules=['src'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'wxPython ==3.0.2.0',
        'SQLAlchemy == 1.0.12',
        'selenium >= selenium-2.53.2',
        'requests',
    	'Kivy==1.9.0',
    	'Pillow==2.6.1',
    	'yattag==1.5.3',
    	'beautifulsoup4==4.4.1',
        'PyPDF2',
        'wand'
    ],
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: eBook management',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
    ],
    
    # What does your project relate to?
    keywords='ebook management ',
    package_data={'src.static': ['*.json'],'src.images':['*.png']},
    include_package_data=True
    )
