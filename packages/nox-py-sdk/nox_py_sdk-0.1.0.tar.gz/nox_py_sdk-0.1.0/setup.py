from setuptools import setup, find_packages

setup(
    name="nox-py-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    description="An SDK made with Python to interact with the Checkout API and V2 API in a simple and efficient way.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Rafael Faria",
    author_email="rafael@capyba.com",
    # url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
