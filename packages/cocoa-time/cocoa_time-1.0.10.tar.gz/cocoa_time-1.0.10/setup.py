from setuptools import setup

with open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name="cocoa_time",
    version="1.0.10",
    author="Edanick",
    description = "A cocoa core data timestamp library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.0'
)