from setuptools import setup, find_packages

setup(
    name="EBIOXP0919",
    version="0.1",
    description="Python interface to interact with EBIOXP0919-4I4O board using Raspberry Pi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ElectronBits",
    author_email="info@electronbits.com",
    project_urls={ 
        'Website': 'https://www.electronbits.com',
        'Source': 'https://github.com/electronbits/Py_EBIOXP0919',
    },
    packages=find_packages(),
    install_requires=[
        "smbus",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
