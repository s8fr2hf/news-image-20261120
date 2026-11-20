# The World in One Picture — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/s8fr2hf/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/s8fr2hf/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One front page for one day: Friday 20 November 2026, five stories,
one planet. The lead is Washington, where President Trump says he
will not decide on fresh strikes against Iran until after the new
year. Below it, Europe says it is ready to negotiate with Russia,
Cyclone Akvan comes ashore in Odisha, Voyager 1 sails past one
light-day from Earth, and Seoul's top court overturns a 15-year
sentence for a former prime minister.

The poster is drawn entirely by code — no photographs, no copied
artwork. `render.py` lays out the broadsheet with Pillow and the
DejaVu typefaces: masthead, lead story, a four-story grid, and a
small line-art globe. Every headline was checked against wire
reporting from Reuters, Yonhap, the India Meteorological
Department, and NASA before it went on the page. The lead deck
quotes the president's own words from the Reuters interview.

Run it:

```sh
python3 render.py            # redraw entry.png in this directory
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

Rendering is deterministic: run `render.py` twice and the two
`entry.png` files are byte-identical. `main.py` uses only the
Python standard library; it copies `entry.png` to the output
directory, the way the kit's starter does.

License: MIT.
