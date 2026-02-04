# LLM Integration: Milestones and Release Roadmap

This document maps the [critical analysis and roadmap](analysis-and-roadmap.md) into **GitHub Milestones** and a **Release plan** for tracking and shipping.

---

## Milestones (create these in GitHub)

Create these under **Issues → Milestones → New milestone**. Use the **Title** as the milestone name and **Description** as below.

| # | Title | Description |
|---|--------|--------------|
| **M1** | Correctness and Honesty | Fix documentation and security narrative. Rewrite architecture and security sections to match actual behavior (auto-add, no confirmation, blacklist-only hard block). Add SECURITY.md with the real security model. |
| **M2** | Instruction and Context | Inject allowlist/blacklist into system prompt; inject minimal runtime context (cwd, git branch); expose thinking budget and include_thoughts via config/env. |
| **M3** | Session and Multi-Turn | Define session abstraction (one session per TUI/CLI); persist or pass last N turns; pass conversation history into runner for multi-turn from the model’s perspective. |
| **M4** | Runner Quality | Single event-handling and response-assembly path; stable response contract (documented and tested); preserve exception types or error codes; add trace id and propagate to logs. |
| **M5** | TUI and UX | Use streaming path in TUI; add visual sandbox pane for commands/outputs; improve error handling (clear messages, distinguish network/auth vs model errors). |
| **M6** | Security (Optional) | Configurable policy (e.g. confirmation before allowlist add, read-only mode); optional confirmation for high-risk patterns (rm -rf, dd, chmod 777). |
| **M7** | Observability | Log token usage; expose session/today cost in UI or CLI; structured tool-call logs (e.g. JSON lines). |
| **M8** | Testing | Runner integration tests (full loop, mocked model, response shape); instruction tests (golden snippets or regression checks for build_agent_instruction). |

---

## Release Plan

Releases are ordered by dependency; later releases depend on earlier ones.

| Version | Name | Scope | Milestone(s) |
|---------|------|--------|--------------|
| **v0.2.0** | Foundation | Docs and prompt correctness; context in instruction. | M1, M2 |
| **v0.3.0** | Session & Runner | Multi-turn session; single runner path; trace id. | M3, M4 |
| **v0.4.0** | TUI & Observability | Streaming TUI; sandbox pane; error handling; token/cost visibility; structured logs. | M5, M7 |
| **v0.5.0** | Hardening | Runner and instruction tests; optional security policies. | M8, M6 |

**Note:** M6 (Security) is optional and can be included in v0.4.0 or v0.5.0 depending on priority.

---

## GitHub issues (created)

| Milestone | Issue | Link |
|-----------|-------|------|
| M1 | #9 | [Correctness and Honesty](https://github.com/guilyx/flourish/issues/9) |
| M2 | #10 | [Instruction and Context](https://github.com/guilyx/flourish/issues/10) |
| M3 | #11 | [Session and Multi-Turn](https://github.com/guilyx/flourish/issues/11) |
| M4 | #12 | [Runner Quality](https://github.com/guilyx/flourish/issues/12) |
| M5 | #13 | [TUI and UX](https://github.com/guilyx/flourish/issues/13) |
| M6 | #14 | [Security (Optional)](https://github.com/guilyx/flourish/issues/14) |
| M7 | #15 | [Observability](https://github.com/guilyx/flourish/issues/15) |
| M8 | #16 | [Testing](https://github.com/guilyx/flourish/issues/16) |

Assign each issue to the matching milestone (M1–M8) after creating the milestones below.

---

## Creating Milestones, Project, and Releases

### Option A: One-shot script (recommended)

From the repo root, with [GitHub CLI](https://cli.github.com/) installed and authenticated with `repo` and `project` scope:

```bash
gh auth refresh -s repo,project   # if needed
./scripts/setup_github_roadmap.sh
```

This script:

- Creates the **8 milestones** (M1–M8) with titles and descriptions from the [Milestones table](#milestones-create-these-in-github).
- Creates a **GitHub Project** named **LLM Roadmap**.
- **Adds issues #9–#16** to that project.
- **Links the project** to the repository.
- **Assigns each issue** to its corresponding milestone.

Use `GITHUB_REPO=owner/repo` if not inferred from `git remote origin`. Use `--dry-run` to print commands without executing.

### Option B: Manual in the GitHub UI

1. **Milestones**: **Issues** → **Milestones** → **New milestone**; create each from the [Milestones table](#milestones-create-these-in-github); then set the milestone on issues #9–#16.
2. **Project**: **Projects** → **New project** → add issues #9–#16 (e.g. by URL or search).
3. **Releases**: **Releases** → **Draft a new release**; use the [Release plan](#release-plan) table for tag and description.

### Create releases

1. **Releases** → **Draft a new release**.
2. Choose a tag (e.g. `v0.2.0`) and title (e.g. `v0.2.0 – Foundation`).
3. Use the **Scope** and **Milestone(s)** from the [Release plan](#release-plan) table for the release notes.
4. Publish when the milestone(s) for that version are done.

---

## Summary

- **8 roadmap issues** (#9–#16) exist on GitHub.
- **Milestones, project, and issue–milestone assignment** can be created in one go with `./scripts/setup_github_roadmap.sh` (requires `gh` with `repo` + `project` scope), or manually in the GitHub UI.
- **4 planned releases** (v0.2.0 → v0.5.0) are documented in the [Release plan](#release-plan); create them in **Releases** when ready.
