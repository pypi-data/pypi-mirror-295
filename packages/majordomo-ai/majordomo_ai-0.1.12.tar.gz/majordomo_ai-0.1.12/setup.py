from setuptools import setup, find_packages

setup(
        name="majordomo_ai",
        version="0.1.12",
        packages=find_packages(),
        install_requires=['Requests>=2.32.3', 'pydantic>=2.7.1']
    )
