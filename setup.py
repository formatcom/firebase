from setuptools import setup, find_packages

setup(
    name = 'firebase',
    packages = find_packages(),
    version = '1.1.0',
    description = "Simple wrapper around Firebase's REST API",
    author = 'Michael Huynh | Vinicio Valbuena',
    author_email = 'mike@mikexstudios.com | vinicio.valbuena89 at gmail dot com',
    url = 'http://github.com/mikexstudios/python-firebase | http://github.com/formatcom/firebase',
    install_requires = ['requests >=1.2.0,<1.2.99'], 
    classifiers = [
        'Programming Language :: Python', 
        'License :: OSI Approved :: BSD License',
    ]
)

