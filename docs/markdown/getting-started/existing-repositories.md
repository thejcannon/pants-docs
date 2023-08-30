# Incremental adoption

---

## Recommended steps

If you have an existing repository, we recommend incrementally adopting to reduce the surface area of change, which reduces risk.

Incremental adoption also allows you to immediately start benefitting from Pants, then deepen adoption at your own pace, instead of postponing benefit until you are ready to make dramatic change all at once.

!!! note "Joining Slack"

    We would love to help you with adopting Pants. Please reach out through [Slack](../getting-help/index.md).

### 1. A basic `pants.toml`

Follow the [Getting Started](index.md) guide to install Pants and [set up an initial `pants.toml`](initial-configuration.md). Validate that running `pants count-loc ::` works properly. If you want to exclude a specific folder at first, you can use the [`pants_ignore`](https://www.pantsbuild.org/docs/reference-global#section-pants-ignore) option.

Add the [relevant backends](../using-pants/concepts/enabling-backends.md) to `[GLOBAL].backend_packages`.

### 2. Set up formatters/linters with basic BUILD files

Formatters and linters are often the simplest to get working because—for all tools other than Pylint— you do not need to worry about things like dependencies and third-party requirements.

First, run [`pants tailor ::`](initial-configuration.md#5-generate-build-files) to generate BUILD files. This tells Pants which files to operate on, and will allow you to set additional metadata over time like test timeouts and dependencies on resources.

Then, activate the [Linters and formatters](../python/python-overview/python-linters-and-formatters.md) you'd like to use. Hook up the `fmt` and `lint` goals to your [CI](../using-pants/using-pants-in-ci.md).

### 3. Set up tests

To get [tests](../python/python-goals/python-test-goal.md) working, you will first need to set up [source roots](../using-pants/concepts/source-roots.md) and [third-party dependencies](../python/python-overview/python-third-party-dependencies.md).

Pants's [dependency inference](../using-pants/concepts/targets.md) will infer most dependencies for you by looking at your import statements. However, some dependencies cannot be inferred, such as [resources](../using-pants/assets.md).

Try running `pants test ::` to see if any tests fail. Sometimes, your tests will fail with Pants even if they pass with your normal setup because tests are more isolated than when running Pytest/unittest directly:

- Tests run in a sandbox, meaning they can only access dependencies that Pants knows about. If you have a missing file or missing import, run `pants dependencies path/to/my_test.py` and `pants dependencies --transitive path/to/my_test.py` to confirm what you are expecting is known by Pants. If not, see [Troubleshooting / common issues](../using-pants/troubleshooting.md) for reasons dependency inference can fail.
- Test files are isolated from each other. If your tests depended on running in a certain order, they may now fail. This requires rewriting your tests to remove the shared global state.

You can port your tests incrementally with the `skip_tests` field:

```python title="project/BUILD"
python_tests(
    name="tests",
    # Skip all tests in this folder.
    skip_tests=True,
    # Or, use `overrides` to only skip some test files.
    overrides={
        "dirutil_test.py": {"skip_tests": True},
        ("osutil_test.py", "strutil.py"): {"skip_tests": True},
    },
)
```

`pants test ::` will only run the relevant tests. You can combine this with [`pants peek`](../using-pants/project-introspection.md) to get a list of test files that should be run with your original test runner:

```
pants --filter-target-type=python_test peek :: | \
  jq -r '.[] | select(.skip_tests== true) | .["sources"][]'
```

You may want to [speed up your CI](../using-pants/using-pants-in-ci.md) by having Pants only run tests for changed files.

### 4. Set up `pants package`

You can use `pants package` to package your code into various formats, such as a [PEX binary](../python/python-goals/python-package-goal.md), a [wheel](../python/python-goals/python-package-goal.md#create-a-setuptools-distribution), an [AWS Lambda](../python/python-integrations/awslambda-python.md), or a [zip/tar archive](../using-pants/assets.md).

We recommend manually verifying that this step is working how you'd like by inspecting the built packages. Alternatively, you can [write automated tests](../python/python-goals/python-test-goal.md) that will call the equivalent of `pants package` for you, and insert the built package into your test environment.

### 5. Check out writing a plugin

Pants is highly extensible. In fact, all of Pants's core functionality is implemented using the exact same API used by plugins.

Check out [Plugins Overview](../writing-plugins/index.md). We'd also love to help in the #plugins channel on [Slack](../getting-help/the-pants-community/index.md).

Some example plugins that users have written:

- Cython support
- Building a Docker image with packages built via `pants package`
- Custom `setup.py` logic to compute the `version` dynamically
- Jupyter support

## Migrating from other BUILD tools? Set custom BUILD file names

If you're migrating from another system that already uses the name `BUILD`, such as Bazel or Please, you have a few ways to avoid conflicts:

First, by default Pants recognizes `BUILD.extension` for any `extension` as a valid BUILD file. So you can use a name like `BUILD.pants` without changing configuration.

Second, you can [configure](doc:reference-global#section-build-patterns) Pants to use a different set of file names entirely:

```toml title="pants.toml"
[GLOBAL]
build_patterns = ["PANTSBUILD", "PANTSBUILD.*"]

[tailor]
build_file_name = "PANTSBUILD"
```

And finally you can configure Pants to not look for BUILD files in certain locations. This can be helpful, for example, if you use Pants for some languages and another tool for other languages:

```toml title="pants.toml"
[GLOBAL]
build_ignore = ["src/cpp"]
```
