from setuptools import setup, find_packages

setup(
    name='my_package_rk',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    description='A short description of the package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/your-repo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
