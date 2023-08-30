# fmt

---

See [here](../python-overview/python-linters-and-formatters.md) for how to opt in to specific formatters, along with how to configure them:

- Autoflake
- Black
- Docformatter
- isort
- Pyupgrade
- yapf

If you activate multiple formatters, Pants will run them sequentially so that they do not overwrite each other. You may need to update each formatter's config file to ensure that it is compatible with the other activated formatters.
