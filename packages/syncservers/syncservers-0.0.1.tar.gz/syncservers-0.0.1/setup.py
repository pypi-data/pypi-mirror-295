import setuptools

version = "0.0.1"

with open('README.md', 'r') as fd:
    long_description = fd.read()

setuptools.setup(
    name='syncservers',
    version=version,
    description='instantly sync data among home servers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Zhuo Wang',
    author_email='zhuowang10@gmail.com',
    url='https://github.com/zhuowang10/syncservers',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['syncservers'],
    python_requires='>=3.7, <4',
    install_requires=[
        'easyschedule>=0.107',
        'asyncinotify>=4.0.9',
    ],
)
