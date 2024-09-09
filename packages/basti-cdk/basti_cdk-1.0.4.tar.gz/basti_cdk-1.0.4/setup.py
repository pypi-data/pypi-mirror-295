import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "basti-cdk",
    "version": "1.0.4",
    "description": "Cost-efficient bastion host with a CLI tool for convenient access to your AWS resources",
    "license": "MIT",
    "url": "https://github.com/basti-app/basti/tree/main/packages/basti-cdk",
    "long_description_content_type": "text/markdown",
    "author": "BohdanPetryshyn<bohdan.y.petryshyn@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/basti-app/basti.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "basti_cdk",
        "basti_cdk._jsii"
    ],
    "package_data": {
        "basti_cdk._jsii": [
            "basti-cdk@1.0.4.jsii.tgz"
        ],
        "basti_cdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.86.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
