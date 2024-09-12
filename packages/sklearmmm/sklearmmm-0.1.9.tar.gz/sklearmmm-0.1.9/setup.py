from setuptools import setup, find_packages

setup(
    name="sklearmmm",
    version="0.1.9",
    packages=find_packages(),
    include_package_data=True,  # Включаем дополнительные файлы (например, изображения)
    package_data={
        "sklearmmm": ["images/*.png"],  # Указываем, какие файлы включить (все изображения PNG)
    },
    description="Library with get_task function",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="John Doe",
    author_email="johndoe@gmail.com",
    url="https://github.com/johndoe/sklearmmm",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)