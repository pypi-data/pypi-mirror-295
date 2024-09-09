from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='QionHa-test-hello',
    version='0.5',
    packages=find_packages(),
    install_requires=[],
    entrypoints={
        "console_scripts": [
            "test-hello = conda1:test_bayes:hello"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
