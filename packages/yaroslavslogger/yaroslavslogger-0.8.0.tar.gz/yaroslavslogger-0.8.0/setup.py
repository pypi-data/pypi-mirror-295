from setuptools import setup, find_packages

setup(
    name='yaroslavslogger',
    version='0.8.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple package with a greeting function',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['compiled_libraries/*.so'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

