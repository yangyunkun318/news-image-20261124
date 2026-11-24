[![m](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?ref=zhc1s3ge)
[![m](https://make.fun/badge/news-image-20261124/yangyunkun318/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124?ref=zhc1s3ge)
[![m](https://make.fun/badge/news-image-20261124/yangyunkun318/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?ref=zhc1s3ge)

# THE WORLD — 24 November 2026

A newspaper front page summing up the world's news of Tuesday 24 November
2026 in one image (1024x1024 PNG, 128 KB). Entry for
[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124)
($100).

## The six stories

All six were first reported on 24 November 2026 (UTC):

1. **FOUR TANKERS HIT MINES IN HORMUZ** (hero) — Iran says mines struck
   four tankers in the Strait of Hormuz; its army chief orders the waterway
   closed further until Washington meets Tehran's terms.
2. **MYANMAR GUILTY OF GENOCIDE** — The UN court rules the 2017 crackdown
   on the Rohingya was genocide, a first for any state.
3. **ISRAEL KILLS HAMAS SECURITY CHIEF** — Brig. Gen. Naeem Abu Mohammed
   Nahel dies in a strike, despite the October ceasefire.
4. **CAR BOMB HURTS 23** — Blast outside regional offices in
   Villavicencio, Colombia; the president blames narcoterrorism.
5. **EL CHAPO ISIDRO CAPTURED** — A U.S. drone helped Mexican forces seize
   cartel boss Fausto Isidro Meza Flores; 20 die in the raid.
6. **RUSSIAN STRIKE KILLS 2** — Zaporizhzhia hit; 44 wounded, four of them
   children. Moscow says it downed ~700 drones overnight.

Ticker: UK sanctions Yemen's Houthis · Iraq takes control of Kurdish
oilfields · Hasina plans Dec 16 return · Hanoi blast kills six.

## How it runs

`main.ts` (Node 22, standard library only) decodes the pre-rendered
`entry.png` embedded as base64 and writes it to the output directory,
verifying the PNG signature, the 1024x1024 dimensions and the 1 MiB gate:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` is the Pillow program that drew the front page (flat vector
illustration + real text, deterministic — same input, same bytes). Run it
to regenerate `entry.png` from scratch:

```
python3 render.py
```
