from setuptools import setup, find_packages

setup(
    name='utilita',
    version='1.0.13',
    packages=find_packages(),
    url = 'https://github.com/json2d/utilita',
    license= 'MIT', # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    author = 'Jason Yung, Tommy Rojo',
    author_email = 'json.yung@gmail.com, tr.trojo@gmail.com',
    description = 'a utility library', # Give a short description about your library
    long_description = open("README.md").read(),
    long_description_content_type='text/markdown',
    install_requires= ['isoweek', 'pendulum>=2', 'deprecated', 'openpyxl>=3,<4', 'pandas>=1', 'sendgrid>=6.0.0'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License'
    ]
)