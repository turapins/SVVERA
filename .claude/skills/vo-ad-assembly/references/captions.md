# Burned-in captions without a text filter

## What is missing here

This machine's ffmpeg has **no `drawtext`, `subtitles` or `ass`** — only `overlay` and
`drawbox`. And the homebrew `whisper` CLI cannot import (numba wants NumPy ≤2.4, the
python3.14 site-packages has 2.5), so `--word_timestamps` dies before transcribing.

## Alignment

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "model_id=scribe_v1" -F "timestamps_granularity=word" -F "language_code=eng" \
  -F "file=@VO.mp3" -o stt.json
```

Returns per-word `start`/`end` with no reference text. Filter to `type=="word"`.

## Phrasing

Word counts alone produce fragments like *"LISTENING, WHO COULD DO"*. Break on structure:

| | |
|---|---|
| a full stop `.!?` | **always** breaks, whatever the last word is |
| ceiling 7 words or 2.8s | always breaks — otherwise the dangling-word rule runs away |
| a comma, from 2 words | breaks, unless the last word is dangling |
| 5 words or 2.0s | breaks, unless the last word is dangling |

Dangling = articles, prepositions, conjunctions, auxiliaries, pronouns — a caption must
not end on one. Then fold any group under ~0.6s, or of one word, into the group before it,
allowing up to 9 words combined; a smaller ceiling leaves orphans like *"to."* on screen
for 0.68s.

## Look

Montserrat ExtraBold, ~29px on a 480-wide frame (≈6% of width), amber `(250,186,32)` on a
3px near-black outline plus an offset shadow, centred, baseline at ≈0.72·H. No pill: the
outline carries legibility on both a bright kitchen and a dark bedroom, and the pill reads
as a UI element rather than as part of the picture.

A pill (`fill=(0,0,0,200)`, radius 13) is the alternative when captions must sit over a
busy brand banner. Judge it at 100% — a downscaled contact sheet makes a working pill look
absent.

## Gapless

Hold each caption until the next one starts:

```python
for i in range(len(entries)-1):
    entries[i] = (entries[i][0], entries[i+1][0], entries[i][2], entries[i][3])
```

## One overlay, not seventy-six

ffmpeg will not take 76 inputs. Build a single alpha track with the concat demuxer, a
transparent PNG filling the gaps:

```
file 'subs/_blank.png'
duration 0.090
file 'subs/c000.png'
duration 0.940
...
```

```bash
ffmpeg -f concat -safe 0 -i caps.txt -c:v png -pix_fmt rgba -r 24 caps.mov
```

then one `[base][cap]overlay=0:0:shortest=1`. The same route builds end cards and titles.

## Overlay ordering and timing

Banner under captions, captions on top. A still that must appear partway through the
timeline is loaded with `-loop 1`, faded on its **own** clock, and only then shifted:

```
[1:v]scale=480:854,format=rgba,
     fade=t=in:st=0:d=0.4:alpha=1,fade=t=out:st=5.6:d=0.4:alpha=1,
     trim=duration=6,setpts=PTS-STARTPTS+84/TB[b1];
[0:v][b1]overlay=0:0:repeatlast=0:eof_action=pass[o1]
```

Fading after the shift would make `st=` chase the timeline position. `repeatlast=0` and
`eof_action=pass` keep the base visible outside the window.
