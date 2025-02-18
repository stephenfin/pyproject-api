"""
Please keep this file Python 2.7 compatible.
See https://tox.readthedocs.io/en/rewrite/development.html#code-style-guide
"""

import os
import sys
import tarfile
from textwrap import dedent
from zipfile import ZipFile

name = "demo_pkg_inline"
pkg_name = name.replace("_", "-")

version = "1.0.0"
dist_info = "{}-{}.dist-info".format(name, version)
logic = "{}/__init__.py".format(name)
metadata = "{}/METADATA".format(dist_info)
wheel = "{}/WHEEL".format(dist_info)
record = "{}/RECORD".format(dist_info)
content = {
    logic: "def do():\n    print('greetings from {}')".format(name),
    metadata: """
        Metadata-Version: 2.1
        Name: {}
        Version: {}
        Summary: UNKNOWN
        Home-page: UNKNOWN
        Author: UNKNOWN
        Author-email: UNKNOWN
        License: UNKNOWN
        Platform: UNKNOWN

        UNKNOWN
       """.format(
        pkg_name, version
    ),
    wheel: """
        Wheel-Version: 1.0
        Generator: {}-{}
        Root-Is-Purelib: true
        Tag: py{}-none-any
       """.format(
        name, version, sys.version_info[0]
    ),
    "{}/top_level.txt".format(dist_info): name,
    record: """
        {0}/__init__.py,,
        {1}/METADATA,,
        {1}/WHEEL,,
        {1}/top_level.txt,,
        {1}/RECORD,,
       """.format(
        name, dist_info
    ),
}


def build_wheel(wheel_directory, metadata_directory=None, config_settings=None):  # noqa: U100
    base_name = "{}-{}-py{}-none-any.whl".format(name, version, sys.version_info[0])
    path = os.path.join(wheel_directory, base_name)
    with ZipFile(path, "w") as zip_file_handler:
        for arc_name, data in content.items():  # pragma: no branch
            zip_file_handler.writestr(arc_name, dedent(data).strip())
    print("created wheel {}".format(path))
    return base_name


def get_requires_for_build_wheel(config_settings=None):  # noqa: U100
    return []  # pragma: no cover # only executed in non-host pythons


def build_sdist(sdist_directory, config_settings=None):  # noqa: U100
    result = "{}-{}.tar.gz".format(name, version)
    with tarfile.open(os.path.join(sdist_directory, result), "w:gz") as tar:
        root = os.path.dirname(os.path.abspath(__file__))
        tar.add(os.path.join(root, "build.py"), "build.py")
        tar.add(os.path.join(root, "pyproject.toml"), "pyproject.toml")
    return result


def get_requires_for_build_sdist(config_settings=None):  # noqa: U100
    return []  # pragma: no cover # only executed in non-host pythons


if "HAS_REQUIRES_EDITABLE" in os.environ:

    def get_requires_for_build_editable(config_settings=None):  # noqa: U100
        return [1] if "REQUIRES_EDITABLE_BAD_RETURN" in os.environ else ["editables"]


if "HAS_PREPARE_EDITABLE" in os.environ:

    def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):  # noqa: U100
        dest = os.path.join(metadata_directory, dist_info)
        os.mkdir(dest)
        for arc_name, data in content.items():
            if arc_name.startswith(dist_info):
                with open(os.path.join(metadata_directory, arc_name), "w") as file_handler:
                    file_handler.write(dedent(data).strip())
        print("created metadata {}".format(dest))
        if "PREPARE_EDITABLE_BAD" in os.environ:
            return 1  # type: ignore # checking bad type on purpose
        return dist_info


def build_editable(wheel_directory, metadata_directory=None, config_settings=None):
    if "BUILD_EDITABLE_BAD" in os.environ:
        return 1  # type: ignore # checking bad type on purpose
    return build_wheel(wheel_directory, metadata_directory, config_settings)
