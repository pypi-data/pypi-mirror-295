from setuptools import setup, find_packages

setup(
    name="name_recognize",
    version="0.1.0",
    author="SuperUser",
    description="Библиотека для распознавания и нормализации имен на русском языке с поддержкой нескольких стран",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={'name_recognize': ['names_ru.csv']},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
