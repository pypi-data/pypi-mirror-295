from setuptools import setup

name = "types-mysqlclient"
description = "Typing stubs for mysqlclient"
long_description = '''
## Typing stubs for mysqlclient

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`mysqlclient`](https://github.com/PyMySQL/mysqlclient) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`mysqlclient`.

This version of `types-mysqlclient` aims to provide accurate annotations
for `mysqlclient==2.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/mysqlclient. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`9d6fc1dafdf9d27a9ea87e210ff6e287d00a61d5`](https://github.com/python/typeshed/commit/9d6fc1dafdf9d27a9ea87e210ff6e287d00a61d5) and was tested
with mypy 1.11.1, pyright 1.1.379, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.2.0.20240911",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/mysqlclient.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['MySQLdb-stubs'],
      package_data={'MySQLdb-stubs': ['__init__.pyi', '_exceptions.pyi', '_mysql.pyi', 'connections.pyi', 'constants/CLIENT.pyi', 'constants/CR.pyi', 'constants/ER.pyi', 'constants/FIELD_TYPE.pyi', 'constants/FLAG.pyi', 'constants/__init__.pyi', 'converters.pyi', 'cursors.pyi', 'release.pyi', 'times.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
