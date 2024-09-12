import re

import setuptools

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

with open("src/chirpstack_rest_api_client/__init__.py", "rt") as fh:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", fh.read()).group(1)

setuptools.setup(
    name="chirpstack_rest_api_client",
    version=version,
    author="Alexandr Korochkin",
    author_email="ka1ll1cit@gmail.com",
    description="A client for interacting with the Chirpstack REST API",
    license="Apache License, Version 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/AlKorochkin/chirpstack-rest-api-client",
        "Bug Tracker": "https://github.com/AlKorochkin/chirpstack-rest-api-client/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["httpx==0.27.2", "pydantic==2.9"],
)
