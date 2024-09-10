import setuptools
from pathlib import Path

setuptools.setup(
    # Keep this name unique so that it does not conflict with other packages in pypi.org
    name="sid7188pdf",
    version=1.0,
    # This should have the content of the README file
    long_description=Path("README.md").read_text(),
    # so we need to tell what packages rg going to be distributed. Because in this project we currently have
    # one package sidpdf and it has 2 .py files pdf2text.py n pdf2image.py
    # so we need to tell setup tools about d modules n packages that we r going to publish
    # find_packages() method will look at ur project n automatically discover packages that we have defined
    # However, we need to tell it to exclude 2 directories - tests n data because they dont include d source code

    packages=setuptools.find_packages(exclude=["tests", "data"])
)
