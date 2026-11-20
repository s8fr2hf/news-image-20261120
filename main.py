"""Entrypoint for the news-image-20261120 entry.

The poster itself is drawn by render.py and shipped in this
repository as entry.png. This program copies that image to the
output directory, mirroring the kit starter's approach: the
grader runs the program with no network and only the standard
library, so the entrypoint itself uses nothing but the standard
library.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(output_dir, "entry.png"))


if __name__ == "__main__":
    main()
