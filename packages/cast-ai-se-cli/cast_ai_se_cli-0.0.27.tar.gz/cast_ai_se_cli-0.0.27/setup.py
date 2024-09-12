from setuptools import setup, find_packages
import os

with open(os.path.join('version.txt')) as version_file:
    version_from_file = version_file.read().strip()

with open('requirements.txt') as f_required:
    required = f_required.read().splitlines()

with open('test_requirements.txt') as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="cast-ai-se-cli",
    author="Dan Amzulescu",
    author_email="dan@cast.ai",
    description="Provides a CLI to run all sorts of sequences like demo prep.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    test_suite='nose.collector',
    test_requires=required_for_tests,
    package_data={'': ['*.txt']},
    install_requires=required,
    version=version_from_file,
    include_package_data=True,
    keywords="cast command-line cli",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={"console_scripts": ["se-cli=cli.shell:main"]},
    python_requires=">=3.11",
)
