# Spiral + Meta query recipes for the research step

All Spiral tools are read-only and, as of 2026-09-03, priced 0.0 credits (`mcp__spiral__usage`
shows `price: "0.0"` on every call). Check `usage` once at the start of a session anyway and
report the count in chat; if pricing has changed, stop and tell Ivan before continuing.

Cache every result under `context/winning-ads/evidence/<YYYY-MM-DD>/` before reading it. Large
results (collections, transcripts, `ads_details`) are saved to a file by the harness; parse with
`jq`, never paste them into chat.

## Fixed identifiers

| thing | id |
|---|---|
| Vocal Image brand | `5c4d9e53-4624-4e66-829a-03b75a616e27` |
| page "Vocal Image App" (installs; web scripts moved here from Jul 2026) | `502a9d65-8aa2-4606-b18d-3d6ed7c10bee` |
| page "Speak with Impact" (web, BASIC/PRO family) | `20965345-cedd-41a1-ba44-8f01e9ca82d4` |
| page ab3334bd (catalog carousels) | ignore for scripts |
| Vocal Image TikTok page | `a5f4ee17-e72f-4ef3-ad52-ee1910ad5c2b` |
| RiseGuide brand = VI web persona pages (buildcharisma.com) | `8ba3dc4b-251e-4035-a994-3638de71ef46` |
| persona pages: Charisma Academy / Michelle Lee / Anna Jones / Robert Smith | `52d2c169-c9f8-4ef8-9f8a-ef79824e6fb9` / `63cbc201-cce6-42d9-9a6f-9590f5b79043` / `496c9842-463b-4eff-bff0-3b56647f6b3d` / `6e7f4d7a-ca18-48c7-8a77-dd5cc07d2d0d` |
| competitors | BoldVoice `29517d76-82ba-40db-9961-a3af7f57f847` · Loora `1d37f116-cafb-4fbe-b95d-ed800b982335` · Patter AI `f7ae37e1-c5ce-4cd2-9a9d-2867509c58f6` · Fluently `0700a405-2ab2-4827-ab07-e082a25337f3` · ELSA `448d37aa-b774-4664-aaa4-f7431aeadc2a` |
| Meta ad accounts (EUR) | iOS-01_main `995418495204994` · Android-01 `608292283693683` · Web-01 (communication) `983605890004213` · Web-02 `321169920479128` · Web 05 (voice) `1007358178403669` |

## Recipe 1 — current state of Vocal Image (run every time, ~6 calls)

```
mcp__spiral__usage                                                    # quota, report count
mcp__spiral__brand_winners  brand_uuid=<VI> creative_type=VIDEO limit=25             # sort winning_score
mcp__spiral__brand_winners  brand_uuid=<VI> creative_type=VIDEO limit=15 sort=active_days
mcp__spiral__meta_page_ads  meta_page_uuid=<Vocal Image App> sort=duration creative_type=VIDEO limit=15 from_date=<today-180d>
mcp__spiral__meta_page_ads  meta_page_uuid=<Speak with Impact> sort=duration creative_type=VIDEO limit=10 from_date=<today-180d>
mcp__spiral__brand_winners  brand_uuid=<RiseGuide> creative_type=VIDEO limit=10      # empty since Aug 2026; if non-empty, the persona pages are back
```
Write down: the top 5 `body` lines (Meta primary text = the hook family), `active_days`,
`duplicate_count`, `cta_text`, `start_date`. New body text you have not seen = a new hook
family; transcribe it (Recipe 3) before writing.

## Recipe 2 — competitor state (~3 calls)

```
mcp__spiral__brand_winners brand_uuid=<BoldVoice> creative_type=VIDEO limit=8
mcp__spiral__brand_winners brand_uuid=<Loora>     creative_type=VIDEO limit=8
mcp__spiral__brand_winners brand_uuid=<Patter AI> creative_type=VIDEO limit=8
```
Only act on `proven_winner` / `strong_winner` bands with `active_days ≥ 45`. Note the opening
line and the proof mechanism. If Ivan pasted a competitor ad URL: `ads_search` won't take a URL;
ask for the Spiral uuid or run `brands_search` on the brand name → `brand_winners`.

## Recipe 3 — read an ad (per ad, cached on repeat)

```
mcp__spiral__transcribe_ads      uuids=[≤10]        # word-timed; hook = segments with end ≤ 3 s
mcp__spiral__ad_creative_analysis ad_uuid=<one>     # hook mechanism, structural_arc with timestamps, proof, CTA
```
Parse transcripts from the saved file:
```bash
jq -r '.data[] | "### "+.ad_uuid+"\n"+([.transcript.segments[]? | "["+(.start|tostring)+"-"+(.end|tostring)+"] "+.text]|join("\n"))' <saved.json>
```
The first structural cut is `structural_arc[1].start_seconds`. Brand mention timing is
`branding.brand_name_spoken_timestamps_seconds`.

## Recipe 4 — Ivan's own collections (free)

`mcp__spiral__my_collections` → `collection_ads collection_uuid=<…> limit=20`. Known: "winners"
`c79c00ed-07ad-4280-8229-e5534bad6204` (12 competitor refs), "new web 17JUN"
`5803854b-9a85-4b4c-9f13-4563bff729ba` (VI persona-page web ads), "IN APP INSTALLS"
`ee8dfb8c-49c6-4774-b5fd-a8269742916e` (Headway/Master English install statics — adjacent, not
category). Payload arrives as `[{type,text}]`; the JSON is the element whose text starts with `{`:
```bash
jq -r '[.[]|.text|select(startswith("{"))]|.[0]' <saved> | jq -r '.meta_ads[]|[.uuid[:8],.meta_page.name,.start_date[:10],.end_date[:10],.cta_text,(.body//""|.[:100])]|@tsv'
```

## Recipe 5 — Meta performance (the only [MEASURED] source)

Always sorted and limited (see `feedback_rework_cost_optimization` memory). Keep one
`client_conversation_id` per session.
```
ads_get_ad_entities ad_account_id=<iOS-01_main> level=ad
  fields=[name, amount_spent, omni_purchase, cost_per_omni_purchase, impressions, ctr,
          video_play_actions, video_thruplay_watched_actions, video_p50_watched_actions,
          video_p100_watched_actions, video_avg_time_watched_actions]
  time_range={"since":"<today-90d>","until":"<today>"} sort=amount_spent_descending limit=25
```
Web-01 / Web-02 at **ad level timed out 6/6 times on 2026-09-03** at every size, including
limit 8 / last_7d / 3 fields. Campaign level (`level=campaign`, 4 fields, limit 10) works. Try
ad level once with `limit=12`, `date_preset=last_30d`, 4 fields; if it fails, fall back to
campaign level plus the per-creative numbers in the team's script doc, and say so in the report.
Field names: `omni_purchase` (alias purchases), `cost_per_omni_purchase`; `hook_rate` and
`mobile_app_installs` do not exist in this catalog.

Derived rates worth writing down when the video fields are populated:
thruplay/plays, p50/plays, p100/plays, avg watch seconds. Only two iOS rows had them in Sep 2026.

## Recipe 6 — the team's own scripts

TST_IVAN_04 doc id `1H3F-yM6v8kwoJVBadViSCFOKJXYSPrUkKhrxjapGbBI` (200k chars; `read_file_content`
saves to a file). Script codes are written with escaped underscores (`IT\_TST\_80\_A`):
```bash
jq -r '.fileContent' <saved> > doc.txt
grep -n "NEW TARGET" doc.txt          # every rework's purchases/CPA line
grep -nE "^\**(IT|KR)\\\\_TST" doc.txt  # script headings
```
Other docs: see `reference_script_docs_library` memory (Kirill's KR_TASKS is view-only).

## Quota and reporting

End every research step with one chat line: "Spiral: N calls, 0 credits. Meta: M calls (K
failed). Cached under evidence/<date>/." If `usage` ever shows a non-zero price, stop.
