from setuptools import setup, find_packages

setup(
    name="hitss_glpi",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "selenium",
        "webdriver-manager"
    ],
    entry_points={
        "console_scripts": [
            "hitss_glpi=hitss_glpi.api:main",
        ],
    },
    author="hhportugames",
    author_email="my@mundilinux.xyz",
    description="A Python library to interact with GLPI API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/De0xyS3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
