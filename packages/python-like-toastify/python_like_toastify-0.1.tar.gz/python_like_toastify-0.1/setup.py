from setuptools import setup, find_packages

setup(
    name='python-like-toastify',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A Django reusable app to display customizable toast messages.',
    author='Dean Vervaeck',
    author_email='dean.vervaeck@spotgroup.be',
    url='',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'Django',
    ],
)
