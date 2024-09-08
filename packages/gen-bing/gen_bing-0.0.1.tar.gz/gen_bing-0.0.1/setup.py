from setuptools import find_packages, setup

setup(
    name="gen_bing",
    version="0.0.1",
    author="Lucifer",
    author_email="ikyodeos01@gmail.com",
    description="First Library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jonesroot/gen_bing",
    packages=find_packages(),
    install_requires=["aiofiles>=23.2.1", "httpx[http2]"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="gabut",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "bing-create = bing_create.main:main",
        ],
    },
    project_urls={
        "Documentation": "https://github.com/jonesroot/gen_bing",
        "Source": "https://github.com/jonesroot/gen_bing",
    },
)
