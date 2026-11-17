# Microsoft Ignite 2026 roundup

**Everything Microsoft announced at Ignite 2026 so far, in plain English: the best announcements, what you can use today, and what it means for 2027.** It's built as an open dataset with an interactive page and a LinkedIn carousel.

| | |
|---|---|
| ![Overview cover](outputs/overview_slides/slide_01.png) | ![Key moment](outputs/overview_slides/slide_02.png) |

## The overview: key moments from the keynote, and what they mean

[`outputs/overview.html`](outputs/overview.html) is a visual overview built around stills from the keynote:

- **Copilot becomes the place work starts.** One conversation spans Salesforce, Outlook and Teams.
- **Autopilot keeps working.** You give it standing instructions and approve what it produces.
- **Office documents come out of a conversation.** Office in Copilot is generally available.
- **Microsoft's own models go head to head.** Microsoft-Decision-1.1 scores six points higher and runs 2.2x faster than version 1.
- **Trust gets its own slide.** Microsoft announced the AI Transparency Initiative.
- **AI's physical footprint becomes a keynote topic.** Microsoft set out a community-first data centre plan.

It then zooms out to **five forces shaping work in 2027** and **the skill to build in each role**, with a [LinkedIn carousel](outputs/linkedin_overview_carousel.pdf) and [post copy](LINKEDIN_POST_OVERVIEW.md).

## Day 1 in four lines

- **Copilot takes centre stage.** Microsoft now calls it "the new operating system for work". Word, Excel and PowerPoint open inside it, and agents (Autopilot, Workspaces, Copilot Code) work on tasks for you.
- **Agents get managed.** Agent 365 adds identities, cost controls and performance analytics for AI agents.
- **Microsoft's own AI.** New MAI models for code, security, images and decisions, the Maia 300 chip and Cobalt 200 servers.
- **Security first.** Microsoft Perception's security agents, Entra Agent ID, and Purview controls that keep Copilot away from sensitive files.

## What the data says

I logged **34 headline announcements** from Day 1 and tagged each one by area, availability and who it's for.

| | |
|---|---|
| ![](outputs/charts/1_announcements_by_area.png) | ![](outputs/charts/2_who_benefits.png) |

- Only **11 of 34 (32%)** are available today. The rest are in preview (13), early access (5) or announced as coming (5).
- **Developers** got the most they can use now (6 of 12). **Everyday workers** got 2 of 11, so the headline Copilot features will roll out over the coming months.

## What it means going forward

1. **Copilot is becoming the operating system for work.** The skill that matters shifts from knowing your way around Office to directing agents.
2. **Microsoft is building its own AI stack.** It now has its own models and chips, alongside OpenAI and Meta models.
3. **Agents are being managed like employees.** They get identities, budgets, performance reviews and security cover.
4. **Copilot is opening up to other vendors' tools.** Salesforce runs in Copilot, Fabric data works in ChatGPT and Claude, and there are 350+ connectors.
5. **Trust is now part of the pitch.** Microsoft announced transparency standards and tighter data controls.

The interactive page is in [`outputs/roundup.html`](outputs/roundup.html). Open it in a browser to filter announcements by your role and by availability.

## Project structure

```
data/announcements.json   Curated dataset: every headline announcement, tagged by area, availability and audience
data/announcements.csv    The same data, flat (generated)
src/analyze.py            Summary stats + charts      -> outputs/summary.json, outputs/charts/
src/build_page.py         Interactive roundup page    -> outputs/roundup.html
src/carousel.py           LinkedIn carousel (1080x1350) -> outputs/linkedin_carousel.pdf, outputs/slides/
src/build_overview.py     Visual overview page        -> outputs/overview.html (uses data/outlook.json, data/keynote_moments.json)
src/overview_carousel.py  Overview carousel           -> outputs/linkedin_overview_carousel.pdf, outputs/overview_slides/
LINKEDIN_POST.md          Post copy
```

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd src && python analyze.py && python build_page.py && python carousel.py
```

To add Day 2 to Day 4, append items to `data/announcements.json` and rerun the three scripts.

## Sources and method

- [Microsoft Ignite 2026 Book of News](https://news.microsoft.com/events/ignite/2026/book-of-news/), the [Microsoft Source overview](https://news.microsoft.com/source/2026/11/17/microsoft-ignite-2026-empowering-human-ambition-intelligence-and-trust/) and the [live news page](https://news.microsoft.com/events/ignite/2026/live-news/).
- Availability labels follow Microsoft's wording. "Early access" covers the Frontier programme and private previews.
- A few keynote figures (50M+ agents in Agent 365, Maia 300 efficiency, GPT-6.2 coming to Foundry) come from press coverage of the keynote ([Technology Record](https://www.technologyrecord.com/article/microsoft-ignite-2026-satya-nadella-predicts-rise-of-the-software-factory), [Windows Forum](https://windowsforum.com/news/microsoft-ignite-2026-keynote-copilot-agents-ai-security-and-azure-launches-explained.452746/)) and are labelled as such.
- The list is a curated set of headline announcements, not an exhaustive count. "What it means" and "best of" are my analysis.

## Related

- [ignite-2026-briefing](https://github.com/Osman246/ignite-2026-briefing): the same announcements framed for business leaders, checked against US Census data on AI adoption.

## License

Code: MIT. Dataset and analysis text: CC BY 4.0. This is an independent analysis, not affiliated with Microsoft.

**Keynote images** in `outputs/img/` (and the slides that use them) are stills from Microsoft's official Ignite 2026 keynote replay, © Microsoft. They're used here for commentary and are **not** covered by the licences above.
