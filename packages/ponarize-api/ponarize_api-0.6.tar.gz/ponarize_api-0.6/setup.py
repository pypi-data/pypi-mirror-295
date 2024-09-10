from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ponarize_api',
    version='0.6',
    description='Relevant, accurate and fast classification of Domains. Blacklist control for aggressive IPs.',
    long_description=long_description,
    long_description_content_type="text/markdown",  # README.md
    author='PonaTech',
    author_email='info@pona.com.tr',
    packages=find_packages(),
    install_requires=[],
)
