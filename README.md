# One image summing up 23 November's world news

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/muhamadlangg71-prog/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/muhamadlangg71-prog/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A program that draws a newspaper-style front page summing up Monday
23 November 2026 in one 1024×1024 image: the tanker strikes in the
Strait of Hormuz lead, with the Russian warship sunk off Libya, the
Democrats' biggest US House majority since 1992, the AI-stock sell-off
in Seoul, the WHO's plea over Ebola in DR Congo, the COP31 fallout, and
a Monday markets ticker.

## Run

```sh
python3 render.py          # draws entry.png (PIL, no AI image generator)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to /output
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. `render.py` is the program that draws the image;
re-running it reproduces `entry.png` byte-identically.

## Stories (all verified, dated 23 November 2026)

- **Lead — Strait of Hormuz:** two oil tankers struck by unknown
  projectiles off Oman on Saturday; a third caught fire on Friday.
  Shipping attacks at their highest level since the US–Iran war began
  (CNN, UKMTO, Reuters).
- **Russian warship sinks off Libya:** corvette Merkury capsized after
  a suspected Ukrainian sea-drone strike at Benghazi; a second
  commercial ship was also hit (Reuters, Fox News).
- **Democrats win biggest House majority since 1992:** at least 258
  seats; Chuck Hubbard beat Virginia Foxx by 330 votes in North
  Carolina after a recount (Reuters, AP, BBC).
- **AI sell-off spreads:** Kospi opened 2.8% lower in Seoul, down
  46.6% from its June peak; S&P 500 in correction, Nasdaq 100 in bear
  market; Seoul readies a 10 trillion won stabilisation fund
  (Korea JoongAng Daily, CNBC/Bloomberg).
- **COP31 fallout:** after the Antalya collapse, diplomats ask whether
  climate diplomacy can recover; 194 nations, no deal (Reuters, AFP).
- **WHO pleads for peace** as fighting disrupts the Ebola response in
  DR Congo (AFP, Al Jazeera).
