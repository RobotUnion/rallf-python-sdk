import setuptools

setuptools.setup(
  name="rallf",
  version="0.3.2",
  author="Lluis Santos",
  author_email="lluis@rallf.com",
  license="MIT",
  description="rallf.com Software Development Kit (SDK)",
  long_description=open("README.md", "r").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/robotunion/rallf-python-sdk",
  packages=setuptools.find_packages(),
  scripts=['bin/rallf'],
  classifiers=[
    "Development Status :: 1 - Planning",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: Developers",
    "Topic :: Software Development",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
  ],
  install_requires=[pkg.strip() for pkg in open("requirements.txt").readlines() if len(pkg) > 1]
)
