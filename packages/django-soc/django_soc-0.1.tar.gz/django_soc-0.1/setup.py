from setuptools import setup, find_packages

setup(
    name='django-soc',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A Django app to log and display user visits.',
    install_requires=[
        'Django>=4.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
