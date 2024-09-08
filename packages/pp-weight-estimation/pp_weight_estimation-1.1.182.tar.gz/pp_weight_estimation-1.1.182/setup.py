#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup,find_packages
import os

VERSION_FILE = os.path.join(os.path.dirname(__file__), "VERSION.txt")
print(VERSION_FILE)

setup(
    name="pp_weight_estimation",
    description="Production planning weight estimation functions",
    author=["Malav Bateriwala"],
    packages=find_packages(),
    #packages=find_packages(),
    scripts=['./scripts/weight_pred.py'],
    install_requires=[
        "mb_base",
        "mb_utils",
        "mb_pandas",],
    setup_requires=["setuptools-git-versioning<2"],
    python_requires='>=3.8',
    setuptools_git_versioning={
        "enabled": True,
       "version_file": VERSION_FILE,
        "count_commits_from_version_file": True,
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}+{branch}",
        "dirty_template": "{tag}.post{ccount}",
    },
)