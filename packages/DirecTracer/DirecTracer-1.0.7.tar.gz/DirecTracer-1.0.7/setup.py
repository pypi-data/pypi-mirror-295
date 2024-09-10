from setuptools import setup, find_packages

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="DirecTracer",
    version="1.0.7",
    author="Hardik Pawar",
    author_email="hardikpawarh@gmail.com",
    description="DirecTracer is a Python script that generates a directory structure in both text and Markdown formats. It can be used to visualize the hierarchy of folders and files in a given directory, while also excluding specific folders and file extensions.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hardvan/DirecTracer",
    keywords=['directory structure', 'visualization',
              'folder hierarchy', 'file organization'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
