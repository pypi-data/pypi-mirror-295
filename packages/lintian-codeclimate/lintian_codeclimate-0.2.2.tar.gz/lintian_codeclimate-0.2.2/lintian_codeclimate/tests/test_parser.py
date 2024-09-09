# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Tests for lintian_codeclimate.parser
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import io
import os
from pathlib import Path

import pytest

from lintian_codeclimate import parser


LINTIAN_EXAMPLES = [
    # simple, one-liner
    pytest.param(
        """
W: package-name: initial-upload-closes-no-bugs [usr/share/doc/package-name/changelog.Debian.gz:1]
""",
        [
            {
                "categories": [
                    "Style"
                ],
                "check_name": "initial-upload-closes-no-bugs",
                "description": (
                    "Initial upload closes no bugs "
                    "[usr/share/doc/package-name/changelog.Debian.gz:1]"
                ),
                "fingerprint": "da2924df3e8386ea4ab1a5d43b37a0d72daa7bda",
                "severity": "minor",
                "type": "issue",
                "location": {
                    "path": "debian/control",
                    "lines": {
                        "begin": 1,
                        "end": 1
                    }
                }
            }
        ],
        id="simple",
    ),
    pytest.param(
        """
N:
W: package-name: initial-upload-closes-no-bugs [usr/share/doc/package-name/changelog.Debian.gz:1]
N:
N:   This package appears to be the first packaging of a new upstream software package (there is only
N:   one changelog entry and the Debian revision is 1), but it does not close any bugs. The initial
N:   upload of a new package should close the corresponding ITP bug for that package.
N:
N:   This warning can be ignored if the package is not intended for Debian or if it is a split of an
N:   existing Debian package.
N:
N:   Please refer to New packages (Section 5.1) in the Debian Developer's Reference for details.
N:
N:   Visibility: warning
N:   Show-Always: no
N:   Check: debian/changelog
N:   Renamed from: new-package-should-close-itp-bug
N:
""",
        [
            {
                "categories": [
                    "Style"
                ],
                "check_name": "initial-upload-closes-no-bugs",
                "description": "Initial upload closes no bugs [usr/share/doc/package-name/changelog.Debian.gz:1]",
                "fingerprint": "da2924df3e8386ea4ab1a5d43b37a0d72daa7bda",
                "severity": "minor",
                "type": "issue",
                "content": {
                    "body": "This package appears to be the first packaging of a new upstream software package (there is only\none changelog entry and the Debian revision is 1), but it does not close any bugs. The initial\nupload of a new package should close the corresponding ITP bug for that package.\n\nThis warning can be ignored if the package is not intended for Debian or if it is a split of an\nexisting Debian package.\n\nPlease refer to New packages (Section 5.1) in the Debian Developer's Reference for details.\n\nVisibility: warning\nShow-Always: no\nCheck: debian/changelog\nRenamed from: new-package-should-close-itp-bug"
                },
                "location": {
                    "path": "debian/changelog",
                    "lines": {
                        "begin": 1,
                        "end": 1,
                    }
                }
            }
        ],
        id="simple-info",
    ),
    # bogus mail host
    pytest.param(
        """
N:
E: example-project changes: bogus-mail-host Changed-By user@Laptop.localdomain
N:
N:   The host part of the named contact address is not known or not globally routables, such as
N:   localhost(.localdomain).
N:
N:   Please refer to Maintainer (Section 5.6.2) in the Debian Policy Manual, Uploaders (Section
N:   5.6.3) in the Debian Policy Manual, and Changed-By (Section 5.6.4) in the Debian Policy Manual
N:   for details.
N:
N:   Visibility: error
N:   Show-Always: no
N:   Check: fields/mail-address
N:   Renamed from: maintainer-address-is-on-localhost uploader-address-is-on-localhost
N:   changed-by-address-is-on-localhost
N:
N:""",
        [
            {
                "categories": [
                    "Style"
                ],
                "check_name": "bogus-mail-host",
                "description": "Bogus mail host Changed-By user@Laptop.localdomain",
                "fingerprint": "5b0f2f6a28c16c0f565e50b04e654362183feccf",
                "severity": "major",
                "type": "issue",
                "content": {
                    "body": "The host part of the named contact address is not known or not globally routables, such as\nlocalhost(.localdomain).\n\nPlease refer to Maintainer (Section 5.6.2) in the Debian Policy Manual, Uploaders (Section\n5.6.3) in the Debian Policy Manual, and Changed-By (Section 5.6.4) in the Debian Policy Manual\nfor details.\n\nVisibility: error\nShow-Always: no\nCheck: fields/mail-address\nRenamed from: maintainer-address-is-on-localhost uploader-address-is-on-localhost\nchanged-by-address-is-on-localhost"
                },
                "location": {
                    "path": "debian/changelog",
                    "lines": {
                        "begin": 12,
                        "end": 12,
                    }
                }
            }
        ],
        id="bogus-mail-host",
    ),
    pytest.param(
        "N: 4 hints overridden (4 info)",
        [],
        id="overrides",
    ),
]


@pytest.fixture
def example_project(tmp_path):
    cwd = Path.cwd()
    os.chdir(tmp_path)
    debian = tmp_path / "debian"
    debian.mkdir()
    (debian / "changelog").write_text("""
example-project (0.0.1-1) unstable; urgency=low

  * example project

-- Example User <user@example.com>  Mon, 8 Apr 2024 11:05:00 +0100

example-project (0.0.0-1) unstable; urgency=low

  * example project

-- Example User <user@Laptop.localdomain>  Mon, 8 Apr 2024 11:00:00 +0100
""")
    yield tmp_path
    os.chdir(cwd)


def _stream(txt):
    stream = io.StringIO()
    stream.write(txt)
    stream.seek(0)
    return stream


@pytest.mark.parametrize(("txt", "result"), LINTIAN_EXAMPLES)
def test_parse(example_project, txt, result):
    assert parser.parse(
        _stream(txt),
        project_dir=example_project.relative_to(Path.cwd()),
    ) == result
