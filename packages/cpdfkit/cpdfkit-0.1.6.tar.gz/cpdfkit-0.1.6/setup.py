from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='cpdfkit',
    version='0.1.6',
    description='A toolkit for rendering HTML to PDF using Chrome headless.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Uli Toll',
    author_email='cpdfkit@codingcow.de',
    url='https://github.com/codingcowde/cpdfkit', 
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    test_suite='tests',
)
