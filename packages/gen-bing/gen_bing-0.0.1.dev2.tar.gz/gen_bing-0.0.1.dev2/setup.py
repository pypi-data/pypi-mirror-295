from setuptools import find_packages, setup


try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "I'm From Indonesian, and I'm still learning."

setup(
    name="gen_bing",
    version="0.0.1.dev2",
    author="Lucifer",
    author_email="ikyodeos01@gmail.com",
    description="I'm From Indonesian, and I'm still learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["aiofiles>=23.2.1", "httpx>=0.24.1", "aiohttp>=3.8.4"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="bing image generator gabut",
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "gen_bing = cli:main",
        ],
    },
)
