from setuptools import setup, find_packages

long_description = ""
try:
    with open("gdzapi/README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except:
    pass

setup(
    name="gdzapi",
    version="0.2.0",
    author="maybewewill",
    author_email="qq238373@gmail.com",
    description="Python library for parsing GDZ.ru (async and sync)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/maybewewill/gdzAPI",
    install_requires=[
        "requests",
        "pydantic",
        "lxml",
        "beautifulsoup4",
        "aiohttp"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)