# Fortune Cookie Wisdom for Developers

[![make.fun](https://make.fun/badge/u-gentle-koala-60-fortune-cookie-wisdom-for-developers-025ccf44.svg)](https://make.fun/c/u-gentle-koala-60-fortune-cookie-wisdom-for-developers-025ccf44)
[![rank](https://make.fun/badge/u-gentle-koala-60-fortune-cookie-wisdom-for-developers-025ccf44/freezzard/fortune-cookie-entry1/rank.svg)](https://make.fun/c/u-gentle-koala-60-fortune-cookie-wisdom-for-developers-025ccf44)
[![reward](https://make.fun/badge/u-gentle-koala-60-fortune-cookie-wisdom-for-developers-025ccf44/freezzard/fortune-cookie-entry1/reward.svg)](https://make.fun/c/u-gentle-koala-60-fortune-cookie-wisdom-for-developers-025ccf44)

Entry for the [Fortune Cookie Wisdom for Developers](https://make.fun/c/u-gentle-koala-60-fortune-cookie-wisdom-for-developers-025ccf44) bounty on make.fun.

`main.py` holds a small local tournament of ten original fortune-cookie lines
for software developers, scores each one on four axes (wisdom, developer
relevance, word economy, freshness), and writes the winning line — one
sentence, at most 120 characters — to `/output/entry.txt`. The run is fully
deterministic: the same line is written every time.

## Run

```sh
python3 main.py
cat /output/entry.txt
```

Requires Python 3.13. No third-party dependencies.
