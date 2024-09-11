from pathlib import Path

import pkg_resources
from setuptools import find_packages, setup


setup(
    name="s3tokenizer",
    py_modules=["s3tokenizer"],
    version="0.0.1",
    description="Reverse Engineering of Supervised Semantic Speech Tokenizer (S3Tokenizer) proposed in CosyVoice",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    python_requires=">=3.8",
    author="xingchensong",
    url="https://github.com/xingchensong/S3Tokenizer",
    license="Apache2.0",
    packages=find_packages(),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            Path(__file__).with_name("requirements.txt").open()
        )
    ],
    entry_points={
        "console_scripts": ["s3tokenizer=s3tokenizer.cli:main"],
    },
    include_package_data=True,
    extras_require={"dev": ["pytest", "scipy", "black", "flake8", "isort"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
)