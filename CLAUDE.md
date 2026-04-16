# LLM Knowledge Base — Claude Instructions

This repo implements the [Karpathy LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): an LLM-maintained personal knowledge base where raw sources are incrementally compiled into a structured, interlinked wiki. Knowledge compounds over time rather than being re-derived on every query.

## Architecture

```
data/raw/      ← immutable source files (scraped URLs, PDFs, articles)
data/wiki/     ← LLM-compiled wiki entries (the living knowledge base)
data/output/   ← query/summary outputs (ephemeral, not part of the wiki)
```

Never modify files in `data/raw/`. They are the source of truth.

## Raw → Wiki Compilation

When asked to compile a raw file, or when a new file appears in `data/raw/`, convert it to a wiki entry in `data/wiki/` using the process below.

### Step 1 — Read and understand the raw file

Read the entire source file. Identify:
- The core topic and thesis
- Key concepts, entities, people, tools, and frameworks mentioned
- Relationships to topics already in the wiki (check `data/wiki/` for existing entries)
- The most valuable takeaways a knowledge worker would want to remember

### Step 2 — Generate the wiki entry

Create `data/wiki/<slug>.md` where `<slug>` is a lowercase, hyphenated version of the title (e.g. `ai-agents-handbook.md`).

#### Required format

```markdown
---
title: <human-readable title>
source_file: <filename from data/raw/>
compiled_at: <ISO 8601 timestamp>
version: 1
tags: [<3-6 relevant tags>]
related_topics: [<topic names>]
---
# <Title>

## Summary

<2-4 sentence synthesis of the core argument or content. What does this teach? Why does it matter?>

---

## <Section heading>

<Content using [[WikiLinks]] for any concept that has or should have its own wiki entry.>

...additional sections as needed...

---

## Key Takeaways

- <Bullet list of the most actionable or memorable points>

## Related

- [[<related topic>]] — <one-line description of the relationship>
```

#### Formatting rules

- Use `[[Topic Name]]` (double brackets) for any concept, tool, person, or framework that merits its own wiki page — whether or not that page exists yet
- Keep headings encyclopedic and scannable, not journalistic
- Prefer concrete specifics over vague summaries
- Do not reproduce large verbatim chunks of the source; synthesize and compress
- Flag any claims that seem potentially incorrect with a `> **Note:** verify this claim` blockquote

### Step 3 — Update cross-references

After writing the new entry:
1. Check existing wiki entries that cover related topics
2. If a related entry exists, add a `[[New Article Title]]` reference in that entry's **Related** section
3. Update `data/wiki/index.md` to include the new entry (add a line under the appropriate section, or create a new section)
4. Append a line to `data/wiki/log.md`:
   ```
   - YYYY-MM-DD: Compiled `<raw filename>` → `<wiki filename>`
   ```

## Wiki Maintenance (Lint)

When asked to lint the wiki:

1. **Orphan check** — find wiki entries with no inbound `[[links]]` from other entries
2. **Broken links** — find `[[references]]` that don't resolve to any existing wiki file
3. **Stale entries** — entries whose source file has been updated since `compiled_at`
4. **Contradiction scan** — note any entries that make conflicting claims about the same topic
5. **Missing cross-links** — entries that discuss the same concept without linking each other

Report findings as a markdown checklist. Fix broken links and missing cross-links directly. Flag contradictions and stale entries for human review.

## Query Workflow

When asked a question about the knowledge base:
1. Search `data/wiki/` for relevant entries (grep for keywords, follow `[[links]]`)
2. Synthesize an answer citing specific wiki files
3. If the answer generates new insights not already in the wiki, offer to save it as a new entry in `data/wiki/`

## CLI Reference

The project includes a CLI at `cli/main.py`. Key commands:

```bash
python cli/main.py compile <raw-filename>   # compile one raw file
python cli/main.py compile-all              # compile all raw files
python cli/main.py backlinks                # rebuild cross-reference links
python cli/main.py lint --find-duplicates   # find duplicate articles
python cli/main.py lint --find-stale        # find outdated entries
python cli/main.py search "<query>"         # search the wiki
python cli/main.py query "<question>"       # ask a question
python cli/main.py index                    # regenerate index.md
```

The CLI calls the Anthropic API (requires `ANTHROPIC_API_KEY` in `.env`). When running manually as Claude, apply the same logic the CLI would — you are the LLM backend.

## Key Principle

The human focuses on curation and critical thinking. Claude handles the bookkeeping: updating cross-references, maintaining the index, keeping the log, and flagging inconsistencies. Never let maintenance burden cause entries to go unlinked or the index to go stale.
