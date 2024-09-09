# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Parser for Lintian.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

CWD = Path(os.curdir)

CHECK_REGEX = re.compile(
    r"Check: (?P<path>debian\/[\w-]+)?(/)?(field(s)?/(?P<field>[\w-]+))?",
)
PATH_REGEX = re.compile(
    r"\[(?P<path>debian\/[\w-]+)(:(?P<line>\d+))?\]\Z",
)
LINE_REGEX = re.compile(
    r"\A(?P<type>[A-Z]):\s+"
    r"(?P<package>[\w-]+)(\s+(?P<class>(source|changes)))?:\s+"
    r"(?P<tag>[\w-]+)(\s+)?"
    r"(?P<desc>.*)?"
)
NOTES_REGEX = re.compile(
    r"\AN:(\s+)?(?P<content>.*)",
)
NOTES_OVERRIDES = re.compile(
    r"\AN: \d+ hints? overridden",
)
SEVERITY = {
    "I": "info",
    "P": "info",
    "W": "minor",
    "E": "major",
}
TAG_MAP = {
    "ancient-standards-version": {
        "field": "standards-version",
    },
    "bogus-mail-host": {
        "block": None,
        "pattern": r"(localhost|\.localdomain)",
    },
    "bogus-mail-host-in-debian-changelog": {
        "block": None,
        "pattern": r"(localhost|\.localdomain)",
    },
    "capitalization-error-in-description": {
        "field": "Description",
        "pattern": lambda x: x["desc"].split(" ")[0],
    },
    "copyright-refers-to-symlink-license": {
        "block": "license",
        "pattern": "{desc}",
    },
    "duplicate-short-description": {
        "field": "description",
    },
    "insecure-copyright-format-uri": {
        "path": "debian/copyright",
        "field": "format",
    },
    "newer-standards-version": {
        "field": "standards-version",
    },
    "no-newline-at-end": {
        "endoffile": True,
    },
    "no-nmu-in-changelog": {
        "path": "debian/changelog",
    },
    "source-nmu-has-incorrect-version-number": {
        "path": "debian/changelog",
    },
    "package-uses-deprecated-debhelper-compat-version": {
        "block": "Build-Depends",
        "pattern": "debhelper",
    },
    "pypi-homepage": {
        "field": "homepage",
    },
    "python-package-missing-depends-on-python": {
        "field": "depends",
    },
    "python3-script-but-no-python3-dep": {
        "field": "depends",
    },
    "uses-debhelper-compat-file": {
        "path": "debian/compat",
    },
}


def _search(pattern, line):
    if isinstance(pattern, re.Pattern):
        return pattern.search(line)
    return re.search(pattern, line, re.I)


def _get_location_debian(
    stream,
    default=1,
    field=None,
    pattern=None,
    block=None,
    endoffile=False,
):
    """Identify a line range in a stream matching a given field or pattern
    inside a block.
    """
    start = 0
    inblock = block is None
    # if block given, but not field or pattern, match the start of the block
    if block and not (field or pattern):
        pattern = block
    for i, line in enumerate(stream, start=1):
        if block and line.lower().startswith(block.lower()):
            inblock = True
        if not inblock:  # keep looking
            continue
        if pattern and _search(pattern, line):
            return (i, i)
        if field and line.lower().startswith(field):
            start = i
        elif start and not line.startswith(" "):
            break
    if start:
        return (start, i - 1)
    if endoffile:
        return (i, i)
    return (default, default)


def get_location(path, default=1, **hints):
    """Attempt to identify a codeclimate 'location' for a given path
    based on the given hints.
    """
    path = Path(path)

    # if the debian path doesn't exist, but a `.in` template file does exist,
    # use that instead
    if not path.exists() and path.with_suffix(".in").exists():
        path = path.with_suffix(".in")

    def _loc(begin, end):
        return {
            "path": str(path),
            "lines": {
                "begin": begin,
                "end": end,
            }
        }

    # if line number is given explicitly, use it
    if line := hints.get("line", None):
        return _loc(line, line)

    # if given no location hints, just return the default location (line 1)
    if not any(hints.values()):
        return _loc(default, default)

    # otherwise try and open the file and find the correct location based on
    # the given hints
    try:
        with open(path, "r") as file:
            return _loc(*_get_location_debian(file, default=default, **hints))
    except OSError:
        pass

    # fallback
    return _loc(default, default)


def format_issue(params):
    tag = str(params["tag"])
    nicetag = tag.capitalize().replace("-", " ")
    description = f"{nicetag} {params['desc']}"

    fingerprint = hashlib.sha1(
        "".join(map(str, params.values())).encode("utf-8"),
    ).hexdigest()

    # construct basic codeclimate issue
    return {
        "categories": ["Style"],
        "check_name": tag,
        "description": description,
        "fingerprint": fingerprint,
        "severity": SEVERITY.get(params["type"], "info"),
        "type": "issue",
        # include parsed information to assist in updated issues later
        "parsed": params,
    }


def update_issue(issue, project_dir=CWD, note=None):
    params = issue.pop("parsed", {})
    tag = issue["check_name"]

    # find the detailed note (if parsed) and use that fill out
    # the body content, and the location
    loc_params = {
        "path": "debian/control",
    }
    if params.get("package") and params.get("class") is None:
        loc_params["block"] = f"package: {params['package']}"
    if params.get("class") == "changes":
        loc_params["path"] = "debian/changelog"
    loc_params.update(TAG_MAP.get(tag, {}))
    if loc_params.get("pattern") and isinstance(loc_params["pattern"], str):
        loc_params["pattern"] = loc_params["pattern"].format(**params)
    elif loc_params.get("pattern") and callable(loc_params["pattern"]):
        loc_params["pattern"] = loc_params["pattern"](params)
    if note:
        issue["content"] = {"body": note}
        if match := CHECK_REGEX.search(note):
            for key, value in match.groupdict().items():
                if value:
                    loc_params[key] = value

    # match path and line number from description suffix
    if match := PATH_REGEX.search(params["desc"]):
        for key, value in match.groupdict().items():
            if value:
                loc_params[key] = value

    # make path relative to project_dir
    loc_params["path"] = project_dir / loc_params["path"]

    # find location
    issue["location"] = get_location(**loc_params)

    return issue


def parse_stream(stream, project_dir=CWD):
    issues = []
    notes = defaultdict(list)
    currentnote = []
    for line in stream:
        # parse notes
        while match := NOTES_REGEX.match(line):
            if not (
                # ignore overrides summary
                NOTES_OVERRIDES.match(line)
            ):
                content = match.groupdict().get("content", "")
                currentnote.append(content)
            try:
                line = next(stream)
            except StopIteration:  # end of file
                break
        if note := os.linesep.join(currentnote).strip():
            latest = issues[-1]
            # record this note in the list of notes
            # (since lintian only shows each note once)
            notes[latest["check_name"]] = note
            # reset for the next note
            currentnote = []
        if match := LINE_REGEX.match(line):
            params = match.groupdict()
            issues.append(format_issue(params))

    # now that we've parsed everything, update issues based on the parsed notes
    for issue in issues:
        update_issue(issue, project_dir, notes.get(issue["check_name"]))

    return issues


def parse(source, *args, **kwargs):
    if isinstance(source, (str, os.PathLike)):
        with open(source, "r") as file:
            return parse(file, *args, **kwargs)

    return parse_stream(source, *args, **kwargs)


def write_json(data, target):
    if isinstance(target, (str, os.PathLike)):
        with open(target, "w") as file:
            return write_json(data, file)
    return json.dump(data, target)


# -- command-line interface

def create_parser():
    """Create an `argparse.ArgumentParser` for this tool.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Path of lintian report to parse (defaults to stdin stream)",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Path in which to write output JSON report.",
    )
    parser.add_argument(
        "-d",
        "--project-dir",
        default=CWD,
        type=Path,
        help=(
            "Path containing source files for project "
            "(including the debian/ tree)"
        ),
    )
    return parser


def main(args=None):
    parser = create_parser()
    opts = parser.parse_args(args=args)
    lint = parse(
        opts.source or sys.stdin,
        project_dir=opts.project_dir,
    )
    write_json(
        lint,
        opts.output_file or sys.stdout,
    )
