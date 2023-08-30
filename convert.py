import os
import os.path
import re
import shutil
import subprocess
import json

shutil.rmtree("docs/markdown/Releases/versions")
os.remove("docs/markdown/Releases/versions.md")

# Slugify directories
for root, dirnames, _ in os.walk('docs/markdown'):
    for dirname in dirnames:
        os.rename(os.path.join(root, dirname), os.path.join(root, re.sub(r'[^\w\s]', '', dirname).lower().replace(" ", "-")))

# Rename files to `index.md` where appropriate
for root, dirnames, _ in os.walk('docs/markdown'):
    for dirname in dirnames:
        path = os.path.join(root, dirname)
        maybe_index = os.path.join(path, dirname + ".md")
        # Child
        # E.g. getting-help/getting-help.md -> getting-help/index.md
        if os.path.exists(maybe_index):
            os.rename(maybe_index, os.path.join(path, "index.md"))
        # Sibling
        # E.g. getting-help/the-pants-community.md -> getting-help/the-pants-community/index.md
        maybe_index = os.path.join(root, dirname + ".md")
        if os.path.exists(maybe_index):
            os.rename(maybe_index, os.path.join(path, "index.md"))

# Other renames/moves
shutil.copytree("docs/markdown/getting-started/getting-started", "docs/markdown/getting-started", dirs_exist_ok=True)
shutil.rmtree("docs/markdown/getting-started/getting-started")
os.rename("docs/markdown/python/python", "docs/markdown/python/python-overview")
os.rename("docs/markdown/python/index.md", "docs/markdown/python/python-overview/index.md")
os.rename("docs/markdown/helm/helm-overview.md", "docs/markdown/helm/index.md")
os.rename("docs/markdown/writing-plugins/plugins-overview.md", "docs/markdown/writing-plugins/index.md")
os.rename("docs/markdown/contributions/contributor-overview.md", "docs/markdown/contributions/index.md")
os.mkdir("docs/markdown/reference")

# Grab the page slugs (for linking later)
page_by_slug = {}
for root, _, filenames in os.walk('docs/markdown'):
    for filename in filenames:
        if not filename.endswith(".md"):
            continue
        file_path = os.path.join(root, filename)
        with open(file_path, "r") as file:
            text = file.read()
            match = re.search(r'slug: "(.*?)"', text)
            page_by_slug[match[1]] = os.path.relpath(file_path, "docs/markdown")


for root, _, filenames in os.walk('docs/markdown'):
    for filename in filenames:
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(root, filename)
        with open(file_path, "r") as file:
            text = file.read()

        newtext = text

        # Get rid of metadata
        newtext = re.sub(
            r'---.*?title: "(.*?)".*?(excerpt: "(.*?)")?.*?---',
            r'# \1\n\n\2\n\n---\n\n',
            newtext,
            flags=re.DOTALL
        )

        # block:image
        newtext = re.sub(
            r"\[block:image\].*?(https:.*?)\",.*?\"(.*?)\".*?\"caption\":.*?\"(.*?)\".*?\[/block\]",
            r'<figure markdown>![\2](\1 "\2")<figcaption>\3</figcaption></figure>',
            newtext,
            flags=re.DOTALL
        )

        # block: embed
        def unslash_quotes(matchobj):
            return matchobj[1].replace('\\"', '"')
        newtext = re.sub(
            r"\[block:embed\].*?(<iframe.*?</iframe>).*?\[/block\]",
            unslash_quotes,
            newtext,
            flags=re.DOTALL
        )

        # block:parameters
        def replace_parameter_block(matchobj):
            data = json.loads(matchobj.group(1))
            cols, rows = data["cols"], data["rows"]
            assert all(x == "left" for x in data["align"])

            result =  "| " + " | ".join(data["data"][f"h-{i}"] for i in range(cols)) + " |"
            result += "\n"
            result += "| " + " | ".join(":---" for i in range(cols)) + " |"
            result += "\n"
            for x in range(rows):
                result += "| " + " | ".join(data["data"][f"{x}-{y}"].replace("\n", "<br>") for y in range(cols)) + " |"
                result += "\n"
            return result

        newtext = re.sub(
            r"\[block:parameters\](.*?)\[/block\]",
            replace_parameter_block,
            newtext,
            flags=re.DOTALL
        )

        # Code snippet titles
        newtext = re.sub(
            r"```(.*) (.*)",
            r'```\1 title="\2"',
            newtext,
        )

        # Admonitions
        def replace_admonition(matchobj):
            type_ = {
                "📘": "note",
                "👍": "success",
                "🚧": "warning",
                "❗️": "danger",
            }[matchobj[1]]

            lines = "\n".join(f"    {line[2:]}" for line in matchobj[3].splitlines())

            return f'!!! {type_} "{matchobj[2]}"\n{lines}\n'

        newtext = re.sub(
            r"> (📘|👍|🚧|❗️) (.*?)\n((>.*?\n)+)",
            replace_admonition,
            newtext,
        )

        # doc: links
        def replace_doc_link(matchobj):
            slug = matchobj[2]
            if slug.startswith("reference"):
                return f"[{matchobj[1]}](doc:{slug})"

            slug, hashsign, anchor = slug.partition("#")
            target_page = page_by_slug[slug]
            relative_path = os.path.relpath(target_page, start=os.path.dirname(os.path.relpath(file_path, start="docs/markdown")))
            print(file_path, target_page, relative_path)
            return f"[{matchobj[1]}]({relative_path}{hashsign}{anchor})"


        newtext = re.sub(
            r"\[(.*?)\]\(doc:(.*?)\)",
            replace_doc_link,
            newtext,
        )

        # @TODO: Fix the link inside the <figure> in docs/markdown/introduction/testimonials.md

        if newtext != text:
            with open(file_path, "w") as file:
                file.write(newtext)

# Make navs
NAV = [
    {"Introduction": {"dir":"introduction", "sub": [
        "how-does-pants-work",
        "language-support",
        "media",
        "news-room",
        "sponsorship",
        "testimonials",
        "welcome-to-pants",
        "who-uses-pants",
    ]},},
    {"Getting Started": {"dir":"getting-started", "sub": [
        "index",
        "prerequisites",
        "installation",
        "initial-configuration",
        "example-repos",
        "existing-repositories",
        "manual-installation",
    ]},},
    {"Getting Help": {"dir":"getting-help", "sub": [
        {"The Pants Community": {"dir": "the-pants-community", "sub": [
            "code-of-conduct",
            "team",
            "maintainers",
            "contentious-decisions",
        ]}},
        "service-providers"
    ]},},
    {"Using Pants": {"dir":"using-pants", "sub": [
        {"Key Concepts": {"dir": "concepts", "sub": [
            "goals",
            "targets",
            "options",
            "enabling-backends",
            "source-roots",
        ],},},
        "command-line-help",
        "troubleshooting",
        "advanced-target-selection",
        "project-introspection",
        "assets",
        "using-pants-in-ci",
        "setting-up-an-ide",
        {"Remote caching & execution": {"dir": "remote-caching-execution", "sub": [
            "index",
            "remote-caching",
            "remote-execution",
        ],},},
        "environments",
        "generating-version-tags",
        "anonymous-telemetry",
        "restricted-internet-access",
        "validating-dependencies",
    ]},},
    {"Python": {"dir":"python", "sub": [
        # @TODO: These dirs could also likely use a rename
        {"Python Overview": {"dir": "python-overview", "sub": [
            "index",
            # @TODO: These files could likely use a rename
            "python-backend",
            "python-third-party-dependencies",
            "python-lockfiles",
            "python-interpreter-compatibility",
            "python-linters-and-formatters",
            "pex",
            "python-distributions",
        ]}},
        {"Goals": {"dir": "python-goals", "sub": [
            "index",
            "python-check-goal",
            "python-fmt-goal",
            "python-lint-goal",
            "python-package-goal",
            "python-repl-goal",
            "python-run-goal",
            "python-test-goal",
        ]}},
        {"Integrations": {"dir": "python-integrations", "sub": [
            "index",
            "protobuf-python",
            "thrift-python",
            "awslambda-python",
            "google-cloud-function-python",
            "pyoxidizer",
            "jupyter",
        ]}},
    ]},},
    {"Go": {"dir":"go", "sub": [
        "index",
        {"Integrations": {"dir": "go-integrations", "sub": [
            "index",
            "protobuf-go",
        ]}},

    ]},},
    # @TODO: Should this be renamed to JVM? Then the Java/Scala page renamed to Java/Scala?
    {"Java and Scala": {"dir":"java-and-scala", "sub": [
        "jvm-overview",
        "kotlin",
    ]},},
    {"Shell": {"dir":"shell", "sub": [
        "index",
        "run-shell-commands",
    ]},},
    {"Docker": {"dir":"docker", "sub": [
        "index",
        "tagging-docker-images",
    ]},},
    {"Helm": {"dir":"helm", "sub": [
        "index",
        "helm-deployments",
        "helm-kubeconform",
    ]},},
    {"Ad-Hoc Tools": {"dir":"adhoc-tools", "sub": [
        "adhoc-tool",
    ]},},
    {"Writing Plugins": {"dir":"writing-plugins", "sub": [
        "index",
        "macros",
        {"The Target API": {"dir": "target-api", "sub": [
            "index",
            "target-api-concepts",
            "target-api-new-fields",
            "target-api-new-targets",
            "target-api-extending-targets",
        ]}},
        {"The Rules API": {"dir": "rules-api", "sub": [
            "index",
            "rules-api-concepts",
            "rules-api-goal-rules",
            "rules-api-subsystems",
            "rules-api-file-system",
            "rules-api-process",
            "rules-api-installing-tools",
            "rules-api-and-target-api",
            "rules-api-unions",
            "rules-api-logging",
            "rules-api-testing",
            "rules-api-tips",
        ]}},
        {"Common plugin tasks": {"dir": "common-plugin-tasks", "sub": [
            # @TODO: plugins-package-goal is hidden
            "index",
            "plugins-lint-goal",
            "plugins-fmt-goal",
            "plugins-typecheck-goal",
            "plugins-codegen",
            "plugins-repl-goal",
            "plugins-test-goal",
            "plugins-setup-py",
            "plugin-upgrade-guide",
            # @TODO: Missing MD "Plugin helpers", https://www.pantsbuild.org/v2.17/docs/plugin-helpers
        ]}},

    ]},},
    {"Releases": {"dir":"releases", "sub": [
        "changelog",
        "deprecation-policy",
        "upgrade-tips",
    ]},},
    {"Contributions": {"dir":"contributions", "sub": [
        "index",
        {"Development": {"dir": "development", "sub": [
            "index",
            "contributor-setup",
            "style-guide",
            "contributions-rust",
            "internal-rules-architecture",
            "contributions-debugging",
            "running-pants-from-sources",
        ]}},
        {"Releases": {"dir": "releases", "sub": [
            "index",
            "release-strategy",
            "release-process",
            "ci-for-macos-on-arm64",
        ]}},
    ]},},
    {"Tutorials": {"dir": "tutorials", "sub": [
        "test-custom-plugin-goal",
        "create-a-new-goal",
        "advanced-plugin-concepts",
    ]},},
]
def get_dirname(unary_dict):
    return next(iter(unary_dict.values()))["dir"]

def make_nav(base, sections):
    result = []
    for section in sections:
        if isinstance(section, str):
            result.append(section + ".md")
        else:
            assert isinstance(section, dict)
            title, obj = next(iter(section.items()))
            result.append(f"{title}: {obj['dir']}")
            make_nav(f"{base}/{obj['dir']}", obj["sub"])

    with open(f"{base}/.nav.yaml", "w") as file:
        file.write("nav:\n")
        file.write("\n".join(
            [
                f"  - {s}"
                for s in result
            ]
        ))


os.mkdir("docs/markdown/reference/goals")
os.mkdir("docs/markdown/reference/subsystems")
make_nav("docs/markdown", NAV)
with open("docs/markdown/.nav.yaml", "a") as file:
    file.write("\n  - Reference: reference")

with open("docs/markdown/reference/.nav.yaml", "w") as f:
    f.write(
        "nav:\n  - Global Options: global-options.md\n  - Goals: goals\n  - Subsystems: subsystems\n  - Targets: targets"
    )

shutil.copytree("docs_extras", "docs/markdown", dirs_exist_ok=True)

subprocess.check_call(["npx", "prettier", "--write", "docs/"])
