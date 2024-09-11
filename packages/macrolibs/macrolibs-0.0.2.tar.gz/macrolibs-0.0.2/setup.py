from setuptools import setup, find_packages


setup(
    name="macrolibs",
    version="0.0.02",
    packages=find_packages(),
    include_package_data=True,
    author="Casey Litmer",
    author_email="litmerc@msn.com",
    description="All of my macros in one place!",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Casey-Litmer/Utilities",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # List your dependencies here
    ],
    python_requires='>=3.6',
)
