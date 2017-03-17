#!/usr/bin/env python
# -*- coding: latin-1 -*-

""" PBR-based setuptools entrypoint. """

__author__ = 'Jonathan Dye'
__license__ = 'GPLv3'

from setuptools import setup

# monkey-patch out the semantic versioning functionality of pbr
from functools import wraps
import pbr.packaging


@wraps(pbr.packaging.get_version)
def version_from_file(package_name, pre_version=None):
    import os

    version_path = os.path.relpath('VERSION')
    if not os.path.exists(version_path):
        raise RuntimeError("Required version file ({}) missing.".format(os.path.abspath(version_path)))
    else:
        with open(version_path, 'r') as version_file:
            pre_version = version_file.readline().strip()
            return pre_version

pbr.packaging.get_version = version_from_file

setup(
    setup_requires=['pbr'],
    pbr=True,
)

# vim: set ts=4 sw=4 expandtab:
