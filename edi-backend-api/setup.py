from setuptools import setup, find_packages

setup(
    name="edi-customization-layer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "flask-sqlalchemy"
    ]
)
