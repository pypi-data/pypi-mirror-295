import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudsnorkel.cdk-github-runners",
    "version": "0.14.2",
    "description": "CDK construct to create GitHub Actions self-hosted runners. A webhook listens to events and creates ephemeral runners on the fly.",
    "license": "Apache-2.0",
    "url": "https://github.com/CloudSnorkel/cdk-github-runners.git",
    "long_description_content_type": "text/markdown",
    "author": "Amir Szekely<amir@cloudsnorkel.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/CloudSnorkel/cdk-github-runners.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudsnorkel.cdk_github_runners",
        "cloudsnorkel.cdk_github_runners._jsii"
    ],
    "package_data": {
        "cloudsnorkel.cdk_github_runners._jsii": [
            "cdk-github-runners@0.14.2.jsii.tgz"
        ],
        "cloudsnorkel.cdk_github_runners": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.123.0, <3.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
