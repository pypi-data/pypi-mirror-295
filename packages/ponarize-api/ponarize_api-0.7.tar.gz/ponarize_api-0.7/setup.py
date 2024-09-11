from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ponarize_api',
    version='0.7',
    description='Relevant, accurate and fast classification of Domains. Blacklist control for aggressive IPs.',
    long_description=long_description,
    long_description_content_type="text/markdown",  # README.md
    author='PonaTech',
    author_email='info@pona.com.tr',
    packages=find_packages(),
    install_requires=[],
    keywords='We Categorize the Web, api for website, api from website, api key for website, logo api, banking logo api, company logo api,  api key website, api of a website, api of website,  best api for website , create an api for a website,  create an api for your website, Website Category API , Website Logo API , logo api, URL logo api, Webshrinker,  classifies a site into a category, zvelo, brandfetch, url categorization, url category check api,  website category lookup, web categories, url classification dataset', 
)
