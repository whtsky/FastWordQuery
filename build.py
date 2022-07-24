#!/usr/bin/env python3
import json
import os
from pathlib import Path
import subprocess
from typing import List

build_dir = Path("./build")
if not build_dir.exists():
    build_dir.mkdir()


def addons() -> list[Path]:
    dirs = []
    for file in Path("./addons21").glob("*"):
        init = file / "__init__.py"
        if os.path.exists(init):
            dirs.append(file)
    return dirs


def build_all():
    for dir in addons():
        print("building", dir, "...")
        build(dir)


def build(dir: Path):
    out = target_file(dir)
    if os.path.exists(out):
        os.unlink(out)
    subprocess.check_call(
        [
            "7z",
            "a",
            "-tzip",
            "-x!meta.json",
            "-x!tests",
            "-bso0",  # less verbose
            out,
            # package folder contents but not folder itself
            "-w",
            os.path.join(dir, "."),
        ]
    )


def run(cmd):
    subprocess.check_call(cmd, shell=True)


def target_file(dir: Path):
    return os.path.join(build_dir, dir.stem + ".ankiaddon")


def last_build_time(dir: Path):
    out = target_file(dir)
    try:
        return os.stat(out).st_mtime
    except:
        return 0


build_all()
print("all done")
