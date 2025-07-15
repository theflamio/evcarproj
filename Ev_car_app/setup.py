from setuptools import setup, find_packages

setup(
    name='my-python-project',
    version='0.1.0',
    author='Flemming Christensen',
    author_email='secret@mail.com',
    description='A app for calculating of toc for a range of electrical cars',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my-python-project',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'polars==0.20.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)