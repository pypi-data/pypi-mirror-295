from setuptools import setup, find_packages

setup(
    name="sklearmmm",  # Название пакета
    version="0.1.3",
    packages=find_packages(),
    description="Library with econometrics function",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Joe Dohn",
    author_email="joedohn@gmail.com",
    url="https://github.com/johndoe/mylibrary",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)