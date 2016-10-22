from setuptools import setup


setup(
    name='savepagenow',
    version='0.0.7',
    description='A simple Python wrapper for archive.org\'s "Save Page Now" capturing service.',
    author='Ben Welsh',
    author_email='ben.welsh@gmail.com',
    url='http://www.github.com/pastpages/savepagenow/',
    packages=('savepagenow',),
    include_package_data=True,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'six',
        'requests',
        'click',
    ],
entry_points='''
        [console_scripts]
        savepagenow=savepagenow.api:cli
    ''',
)
