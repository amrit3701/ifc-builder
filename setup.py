import setuptools

install_requires = [
    "attrs>=18.2.0",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ifc_builder",
    version="0.0.1",
    author="Amritpal Singh",
    author_email="amrit3701@gmail.com",
    description="Basic utilities to work with IfcOpenShell.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amrit3701/ifc-builder",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
)