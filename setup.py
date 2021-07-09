from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
    'werkzeug',
    'wtforms',
    'flask_wtf',
]

setup(
    name='flask_blog',
    version='0.0',
    description='Personal Blogging Website Project using Flask',
    author='Nicholas Hadiwijaya',
    author_email='nicholaswilliam2307@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)