import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="rallf",
  version="0.0.4",
  author="Lluis Santos",
  author_email="lluis@rallf.com",
  description="rallf.com Software Development Kit",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/robotunion/rallf-python-sdk",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
