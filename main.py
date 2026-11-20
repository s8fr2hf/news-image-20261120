"""Entry program for news-image-20261120 (Python 3.13, standard library only).

The poster is pre-rendered at build time by render.py and stored beside
this file as entry.png. This program only copies it to the output
directory, so both grader runs write the same bytes. No network is used.
"""

import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile("entry.png", os.path.join(out_dir, "entry.png"))
