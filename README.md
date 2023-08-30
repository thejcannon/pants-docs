# Pants Documentation Proof-of-Concept Repo

:wave: I'm trying out porting our documentation from the current [readme.com docs](https://www.pantsbuild.org/docs)
to mkdocs+readthedocs.

- mkdocs: https://www.mkdocs.org/
  - (A whole lotta plugins)
- readthedocs: https://readthedocs.org

## How to run it:

`pipx run --pip-args "-r docs/requirements.txt" mkdocs serve -f docs/mkdocs.yml`

# This repo

## What this repo is

This repo represents a __subset__ of the Pants repo. Specifically the `docs/markdown` subset.
The intent is you could `cp <this repo>/docs <pants repo>/docs` and be 99% done.

The docs files themselves were migrated _automatically_ using `convert.py` at the repo root.
No further changing of the files was done. The intent is we could easily convert our docs to
mkdocs-based docs. Then, we can twiddle as necessary.

In order to get reference documentation working, I also store the output of `help-all` into
`help-all.json` and have checked that in. The intent is this would be run on-the-fly in the real
repo during documentation generation.

Additionally, an emphasis has been placed on a feature-parity _minimum_ with our existing docs.
A best effort is also made to make all existing doc links work after the switch.


## What this repo isn't

Firstly, __this repo isn't meant to imply that our docs would be moving out-fo-repo__. For simplicity,
I carved the docs out of the pantsbuild repo and put them here. Just pretend the rest of the Pantsbuild
repo is also in this repo :smile:.

This repo also isn't anything other than a proof-of-concept.


## How to update

Easy. Wipe clean `docs/markdown`. Copy the Pants repo contents. Then run `convert.py`.

For reference documentation you'll need to check in the `help-all` JSON:

```console
josh@cephandrius:~/work/pants$ pants repl build-support/bin/generate_docs.py
>>> import sys, json
>>> sys.path.append("build-support/bin")
>>> import generate_docs
>>> json.dump(generate_docs.run_pants_help_all(), open("help-all.json", "w"))
```

then copy it here.
