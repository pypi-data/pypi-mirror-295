from setuptools import setup, find_packages

setup(
  name="chkexmpt",
  version="0.1.0",
  packages=find_packages(),
  entry_points={
    "console_scripts": [
      "chkexmpt=chkexmpt.main:main",
    ]
  },
  author="Eric Hoffmann",
  author_email="2ffs2nns@gmail.com",
  description="Check for unintentional security exemptions.",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/2ffs2nns/check-exemptions",
  python_requires=">=3.8",
)
