# Backends

---

Most Pants functionality is opt-in by adding the relevant _backend_ to the `[GLOBAL].backend_packages` option in `pants.toml`. For example:

```toml title="pants.toml"
[GLOBAL]
backend_packages = [
  "pants.backend.shell",
  "pants.backend.python",
  "pants.backend.python.lint.black",
]
```

## Available backends

| Backend                                                   | What it does                                                                                       | Docs                                                                                          |
| :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `pants.backend.build_files.fmt.black`                     | Enables autoformatting `BUILD` files using `black`.                                                |                                                                                               |
| `pants.backend.build_files.fmt.buildifier`                | Enables autoformatting `BUILD` files using `buildifier`.                                           |                                                                                               |
| `pants.backend.build_files.fmt.yapf`                      | Enables autoformatting `BUILD` files using `yapf`.                                                 |                                                                                               |
| `pants.backend.awslambda.python`                          | Enables generating an AWS Lambda zip file from Python code.                                        | [AWS Lambda](../../python/python-integrations/awslambda-python.md)                            |
| `pants.backend.codegen.protobuf.lint.buf`                 | Activate the Buf formatter and linter for Protocol Buffers.                                        | [Protobuf](../../python/python-integrations/protobuf-python.md)                               |
| `pants.backend.codegen.protobuf.python`                   | Enables generating Python from Protocol Buffers. Includes gRPC support.                            | [Protobuf and gRPC](../../python/python-integrations/protobuf-python.md)                      |
| `pants.backend.codegen.thrift.apache.python`              | Enables generating Python from Apache Thrift.                                                      | [Thrift](../../python/python-integrations/thrift-python.md)                                   |
| `pants.backend.docker`                                    | Enables building, running, and publishing Docker images.                                           | [Docker overview](../../docker/index.md)                                                      |
| `pants.backend.docker.lint.hadolint`                      | Enables Hadolint, a Docker linter: <https://github.com/hadolint/hadolint>                          | [Docker overview](../../docker/index.md)                                                      |
| `pants.backend.experimental.codegen.protobuf.go`          | Enables generating Go from Protocol Buffers.                                                       |                                                                                               |
| `pants.backend.experimental.go`                           | Enables Go support.                                                                                | [Go overview](../../go/index.md)                                                              |
| `pants.backend.experimental.java`                         | Enables core Java support.                                                                         | [Java & Scala overview](../../java-and-scala/jvm-overview.md)                                 |
| `pants.backend.experimental.java.lint.google_java_format` | Enables Google Java Format.                                                                        | [Java & Scala overview](../../java-and-scala/jvm-overview.md)                                 |
| `pants.backend.experimental.scala`                        | Enables core Scala support.                                                                        | [Java & Scala overview](../../java-and-scala/jvm-overview.md)                                 |
| `pants.backend.experimental.scala.lint.scalafmt`          | Enables the Scalafmt formatter.                                                                    | [Java & Scala overview](../../java-and-scala/jvm-overview.md)                                 |
| `pants.backend.experimental.python.lint.ruff`             | Enables Ruff, an extremely fast Python linter: <https://beta.ruff.rs/docs/>                        | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.experimental.python.packaging.pyoxidizer`  | Enables `pyoxidizer_binary` target.                                                                | [PyOxidizer](../../python/python-integrations/pyoxidizer.md)                                  |
| `pants.backend.experimental.visibility`                   | Enables `__dependencies_rules__` and `__dependents_rules__`                                        | [Visibility](targets.md#visibility)                                                           |
| `pants.backend.google_cloud_function.python`              | Enables generating a Google Cloud Function from Python code.                                       | [Google Cloud Function](../../python/python-integrations/google-cloud-function-python.md)     |
| `pants.backend.plugin_development`                        | Enables `pants_requirements` target.                                                               | [Plugins overview](../../writing-plugins/index.md)                                            |
| `pants.backend.python`                                    | Core Python support.                                                                               | [Enabling Python support](../../python/python-overview/python-backend.md)                     |
| `pants.backend.python.mixed_interpreter_constraints`      | Adds the `py-constraints` goal for insights on Python interpreter constraints.                     | [Interpreter compatibility](../../python/python-overview/python-interpreter-compatibility.md) |
| `pants.backend.python.lint.autoflake`                     | Enables Autoflake, which removes unused Python imports: <https://pypi.org/project/autoflake/>      | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.bandit`                        | Enables Bandit, the Python security linter: <https://bandit.readthedocs.io/en/latest/>.            | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.black`                         | Enables Black, the Python autoformatter: <https://black.readthedocs.io/en/stable/>.                | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.docformatter`                  | Enables Docformatter, the Python docstring autoformatter: <https://github.com/myint/docformatter>. | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.flake8`                        | Enables Flake8, the Python linter: <https://flake8.pycqa.org/en/latest/>.                          | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.isort`                         | Enables isort, the Python import autoformatter: <https://timothycrosley.github.io/isort/>.         | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.pylint`                        | Enables Pylint, the Python linter: <https://www.pylint.org>                                        | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.pyupgrade`                     | Enables Pyupgrade, which upgrades to new Python syntax: <https://pypi.org/project/pyupgrade/>      | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.lint.yapf`                          | Enables Yapf, the Python formatter: <https://pypi.org/project/yapf/>                               | [Linters and formatters](../../python/python-overview/python-linters-and-formatters.md)       |
| `pants.backend.python.typecheck.mypy`                     | Enables MyPy, the Python type checker: <https://mypy.readthedocs.io/en/stable/>.                   | [typecheck](../../python/python-goals/python-check-goal.md)                                   |
| `pants.backend.shell`                                     | Core Shell support, including shUnit2 test runner.                                                 | [Shell overview](../../shell/index.md)                                                        |
| `pants.backend.shell.lint.shfmt`                          | Enables shfmt, a Shell autoformatter: <https://github.com/mvdan/sh>.                               | [Shell overview](../../shell/index.md)                                                        |
| `pants.backend.shell.lint.shellcheck`                     | Enables Shellcheck, a Shell linter: <https://www.shellcheck.net/>.                                 | [Shell overview](../../shell/index.md)                                                        |
