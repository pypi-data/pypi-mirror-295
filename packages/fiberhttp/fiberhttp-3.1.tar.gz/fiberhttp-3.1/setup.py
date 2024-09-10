from setuptools import setup, find_packages

README_FILE = open('README.md', 'r')
README = README_FILE.read()
README_FILE.close()

setup(
    name='fiberhttp',
    version='3.1',
    author='osmz',
    description='simple high performance http requests library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.github.com/xsxo/fiberhttp',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['certifi>=2017.4.17'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ]
)