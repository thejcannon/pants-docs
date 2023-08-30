# lint

---

The `lint` goal runs both dedicated linters and any formatters in check-only mode:

- Autoflake
- Bandit
- Black
- Docformatter
- Flake8
- isort
- Pydocstyle
- Pylint
- Pyupgrade
- yapf

See [here](../python-overview/python-linters-and-formatters.md) for how to opt in to specific formatters and linters, along with how to configure them.

!!! success "Benefit of Pants: runs linters in parallel"

    Pants will run all activated linters at the same time for improved performance. As explained at [Python linters and formatters](../python-overview/python-linters-and-formatters.md), Pants also uses some other techniques to improve concurrency, such as dynamically setting the `--jobs` option for linters that have it.

!!! success "Benefit of Pants: lint Python 2-only and Python 3-only code at the same time"

    Bandit, Flake8, and Pylint depend on which Python interpreter the tool is run with. Normally, if your project has some Python 2-only files and some Python 3-only files, you would not be able to run the linter in a single command because it would fail to parse your code.

    Instead, Pants will do the right thing when you run `pants lint ::`. Pants will group your targets based on their [interpreter constraints](../python-overview/python-interpreter-compatibility.md), and run all the Python 2 targets together and all the Python 3 targets together.
