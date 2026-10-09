# Design Sources

Checked on 2026-10-09. These are design references, not bundled dependencies or instructions inherited from other repositories. This repository contains independently written instructions and helper code.

| Source | Relevant observation | Choice in this skill |
| --- | --- | --- |
| [OpenAI skill creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) | Skills use a focused entrypoint, supporting references and meaningful executable validation. | Keep selection, narrative, Word and delivery details in separate references. |
| [K-Dense venue-templates](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/venue-templates/SKILL.md) | Current venue and submission-stage rules matter; generic templates are not official formats. | Reopen journal instructions for every task and format only after content review. |
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | Scientific writing connects claims, sources and applicable reporting requirements. | Keep a compact principal-claim map and do not invent author facts. |
| [K-Dense literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md) | Source identification and structured synthesis support literature work. | Require full-paper reading cards instead of abstract-only style imitation. |

The K-Dense project now redirects from `claude-scientific-skills` to `scientific-agent-skills`; its current skill paths are under `skills/`. These references do not establish that a service has been installed or that a manuscript meets any journal's requirements.

Local interface experience informed the Word/Zotero route: use the actual connected MCP, preserve complete live fields, and refresh through Zotero when order/content/style changes. No machine-specific executable path, account configuration or manuscript material is bundled.

The optional extractor uses `import pymupdf`; [PyMuPDF's official changelog](https://pymupdf.readthedocs.io/en/latest/changes.html#changes-in-version-1-24-3-2024-05-09) confirms that module name starts at 1.24.3, which sets the dependency floor.

Deliberate differences from general writing/review frameworks:

- Native agent browsing is the required research layer; no paid research API or external LLM is embedded.
- Recent same-journal papers inform narrative and scientific readership; they are not a source of mandatory formatting rules.
- No complete systematic review, blanket raw-data upload, large audit database or hash manifest is imposed.
- The default change scope is narrative and integration, not new experiments or analysis.
