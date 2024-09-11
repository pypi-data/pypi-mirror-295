# setup.py
from setuptools import setup, find_packages

setup(
    name="django-vite-hmr",
    version="1.0.3",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="A Django app to provide custom template tags.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/django-vite-hmr/django-plugin",
    author="Sachin Acharya",
    keywords="django-vite vite-hmr django-hot-reload",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
