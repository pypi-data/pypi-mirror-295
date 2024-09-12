from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = "Anybyte developer utils"
LONG_DESCRIPTION = (
    "A package that provides utility functions for developer use in Anybyte projects"
)

# Setting up
setup(
    name="anybyte-utils",
    version=VERSION,
    author="Anybyte",
    author_email="<ben@anybyte.ai>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["boto3"],
    keywords=["python", "anybyte", "utils", "developer"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
