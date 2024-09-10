from setuptools import setup, find_packages

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="CPPinator",
    version="1.0.5",
    author="Hardik Pawar",
    author_email="hardikpawarh@gmail.com",
    description="CPPinator is a Python automation script designed for compiling and running multiple C++ files in a specified directory. It simplifies the process of handling multiple C++ programs and provides a clear and organized output for each program's execution along with the execution time for each program.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hardvan/CPPinator",
    keywords=["C++", "automation", "script",
              "compile", "run", "multiple", "programs", "CPPinator"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
