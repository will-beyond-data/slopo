# Five Houses: a strategy playbook

Open `five-houses.html` in any browser. It is a single self-contained file (fonts load from Google Fonts when online).

478 strategies drawn from Billions, Peaky Blinders, Vikings, House of Cards and Suits, organised into 15 chapters by type of strategy. Each play is labelled with its show and episodes and links to a summary of every episode it draws on. All 416 episodes are covered in the episode guide.

## Chapters

1. Intelligence & Reading People
2. Leverage & Kompromat
3. Psychological Warfare & Persuasion
4. Negotiation & Dealmaking
5. Deception & Misdirection
6. Traps, Stings & Setups
7. Alliances, Coalitions & Betrayal
8. Patience, Timing & the Long Game
9. Gambits, Sacrifices & Calculated Risk
10. Seizing & Consolidating Power
11. Narrative, Image & Public Opinion
12. Weaponizing Rules & Institutions
13. Leadership, Loyalty & Managing People
14. Crisis, Defense & Counterattack
15. Asymmetric Warfare & Surprise

## How it was made

- Dialogue for 350 of the 416 episodes came from English subtitle files published in public GitHub repositories (credited in the book's "Sources and method" page).
- The other 66 episodes (Billions seasons 4, 5 and 7, most of season 6, and Vikings season 6) had no subtitles available. Plays from those episodes were written from episode knowledge checked against web search, and are marked "From episode knowledge" in the book.
- Reader passes extracted 1,634 candidate plays and a summary for every episode. A pass for each show assembled 70 season-long and series-long campaigns. A curator for each chapter then selected, merged and edited the final entries and wrote the chapter essays.
- All 440 quotes taken from transcripts were checked word for word against the subtitle text.

## Editing and rebuilding

The content lives in `source/`:

- `curated/<CHAPTER>.json`: chapter essay, principles and plays
- `curated_extra/*.json`: extra plays merged into their chapters at build time
- `episodes.json`: episode titles and summaries
- `front.json`: cover subtitle, "How to use this book" and "Sources and method" pages
- `template.html`: the reader (layout, styles and navigation)

To rebuild after editing:

```
cd source
python3 build.py && python3 wrap.py
```
