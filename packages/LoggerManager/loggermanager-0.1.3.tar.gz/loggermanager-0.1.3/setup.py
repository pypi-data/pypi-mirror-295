from setuptools import setup, find_packages
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='LoggerManager',
    version='0.1.3',
    description='A module that extends the standard Python logging module.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Amgarak',
    author_email='painkiller_97@mail.ru',
    url='https://vk.com/zloboglaz',
    packages=find_packages(),
    install_requires=[

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    keywords='logging logger log management log filtering console logging file logging rotating file handler logger configuration log levels internal logger log formatting python logging log management system logging utilities log rotation custom logging',
    license='Apache License 2.0',
)
