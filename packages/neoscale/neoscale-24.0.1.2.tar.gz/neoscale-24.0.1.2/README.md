Python SDK package for MatrixDC newscale, Serverless GPU based AI platform.
MatrixDC Newscale is a Serverless GPU based AI platform, which provides a high-performance and scalable GPU computing service for AI developers. It supports multiple programming languages, including Python, Java, Go, Node.js, C++, etc.


## Build Instruction
Following https://packaging.python.org/en/latest/tutorials/packaging-projects/.

## Setup local environment
1. Edit ~/.pypirc file to add the following content:

```
[distutils]
index-servers=
  pypi
  testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = neoscale
password = <test-api-token>

[pypi]
repository = https://upload.pypi.org/legacy/
username = neoscale
password = <api-token>
```
