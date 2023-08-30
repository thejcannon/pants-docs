from __future__ import annotations
from enum import Enum

import logging
from collections import defaultdict
import subprocess
import json
import textwrap
from pathlib import Path
from typing import Any, cast

import mkdocs_gen_files
import jinja2

logger = logging.getLogger(__name__)

# @TODO: This was stolen from src/python/pants/help/help_info_extracter.py
class HelpJSONEncoder(json.JSONEncoder):
    """Class for JSON-encoding help data (including option values).

    Note that JSON-encoded data is not intended to be decoded back. It exists purely for terminal
    and browser help display.
    """

    def default(self, o):
        if callable(o):
            return o.__name__
        if isinstance(o, type):
            return type.__name__
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


def to_help_str(val) -> str:
    if isinstance(val, (list, dict)):
        return json.dumps(val, sort_keys=True, indent=2, cls=HelpJSONEncoder)
    if isinstance(val, Enum):
        return str(val.value)
    else:
        return str(val)


with open("help-all.json") as f:
    help_info = json.load(f)


env = jinja2.Environment(
    loader = jinja2.FileSystemLoader("docs/reference_templates"),
    autoescape=False,
)
env.filters["help_str"] = to_help_str
env.filters["filter_out"] = lambda values, *args: [value for value in values if value not in args]
env.tests["goal_subsystem"] = lambda value: value in help_info["name_to_goal_info"]
subsystem_template = env.get_template("subsystem.md")
targets_template = env.get_template("target.md")


global_options = help_info["scope_to_help_info"][""]
with mkdocs_gen_files.open(f"reference/global-options.md", "w") as f:
    f.write(subsystem_template.render(subsystem=global_options, goal_info=None))

navs = defaultdict(list)
for info in help_info["scope_to_help_info"].values():
    if not info["scope"]:
         continue

    parent = "goals" if info["is_goal"] else "subsystems"
    with mkdocs_gen_files.open(f"reference/{parent}/{info['scope']}.md", "w") as f:
        f.write(subsystem_template.render(subsystem=info, goal_info=help_info["name_to_goal_info"].get(info['scope'])))
    navs[parent].append(info['scope'])

for info in help_info["name_to_target_type_info"].values():
    if info["alias"].startswith("_"):
        continue

    with mkdocs_gen_files.open(f"reference/targets/{info['alias']}.md", "w") as f:
        f.write(targets_template.render(target=info))
    navs["targets"].append(info['alias'])


for dirname, filenames in navs.items():
    with mkdocs_gen_files.open(f"reference/{dirname}/index.md", "w") as f:
        f.write("\n".join(f"- [{filename}]({filename}.md)" for  filename in filenames))

    with mkdocs_gen_files.open(f"reference/{dirname}/.nav.yaml", "w") as f:
        f.write("nav:\n")
        f.write("  - index.md\n")
        f.write("\n".join(
            [
                f"  - {s}.md"
                for s in filenames
            ]
        ))
