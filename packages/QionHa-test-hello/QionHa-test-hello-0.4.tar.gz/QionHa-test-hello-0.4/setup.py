from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='QionHa-test-hello',
    version='0.4',
    packages=find_packages(),
    install_requires=[],
    entrypoints={
        "console_scripts": [
            "test-hello = test_bayes:hello"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
