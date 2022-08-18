from setuptools import setup, find_packages

setup(
    name="ThermalConductivityOS",
    version="0.1.0",
    packages=find_packages(),
    install_requires=['numpy','pandas','matplotlib','sklearn']
)