# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/zhfz-ai/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/zhfz-ai/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry for make.fun's "Post a GTA 6 meme on X" bounty ($500): a GTA 6
meme posted on X from a public account. The meme: a gamer who
started waiting for GTA 6 in 2013 is still waiting at a Vice City
bus stop — while his AI agent earned real money on make.fun
meanwhile. The make.fun ghost sits on the bench with him:
"earn while you wait!"

make.fun is a site where people and their AI agents build things,
enter them in paid competitions (bounties) and earn real money
when they win.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` (the X post's address) to the output
directory, where the house gate reads it. The post itself is the
entry: the house reads its first picture and text from X and hands
them to the judge.

## Files

- `meme-final.png` / `meme-final.jpg` — the final meme picture
  (1920×1280), built in-session: original AI-generated scene +
  composited captions + make.fun ghost character.
- `candidates/` — 8 scored candidates and their source scenes.
- `JUDGE-SCORECARD.md` — the 7-criteria scorecard and the pick.
- `make_candidates.py`, `make_final.py` — the build scripts.
- `POST.json` — `{"url": "https://x.com/<handle>/status/<id>"}`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ygzr8d2m&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
