from setuptools import setup

name = "types-python-http-client"
description = "Typing stubs for python-http-client"
long_description = '''
## Typing stubs for python-http-client

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-http-client`](https://github.com/sendgrid/python-http-client) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`python-http-client`.

This version of `types-python-http-client` aims to provide accurate annotations
for `python-http-client==3.3.7`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-http-client. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`65170f4a2ef8dc81d3678624ac2a4610d1c6045e`](https://github.com/python/typeshed/commit/65170f4a2ef8dc81d3678624ac2a4610d1c6045e) and was tested
with mypy 1.11.1, pyright 1.1.379, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="3.3.7.20240910",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-http-client.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['python_http_client-stubs'],
      package_data={'python_http_client-stubs': ['__init__.pyi', 'client.pyi', 'exceptions.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
