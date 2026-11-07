---
name: 3d-scenes-retro
description: Turn a finished (or paused) Blender/3D session into reusable knowledge for the 3d-scenes skill - extract problems, causes, fixes and numbers from the conversation, append rules to lessons/LESSONS.md, write a case study, and propose upgrades to the reference files. Use at the end of every 3D project or when the user says "احفظ اللي تعلمناه", "سوي retro", "حدث السكيل", "save what we learned", "update the knowledge", "خل النظام يتعلم من هالمشروع".
---

# 3D Scenes retro — make the next project faster

The 3d-scenes skill lives next to this one: `../3d-scenes/` (references/, scripts/, case-studies/, lessons/).

## Steps
1. **Collect evidence from this session** (not from memory of general knowledge): every user complaint, its measured cause, the fix, the before → after values, render time per frame, what the user approved.
2. **Classify each item**: area (setup, brief, assets, materials, lighting, motion, camera, quality, render, process), and whether it is new, confirms an existing rule, or contradicts one.
3. **Write rules** to `../3d-scenes/lessons/LESSONS.md` (top of the list), one line each:
   `- [YYYY-MM-DD] [area] Rule — evidence (project) — Candidate|Proven`
   A rule seen once = `Candidate`. A rule that already exists and worked again = mark it `Proven` and note the second project.
4. **Write a case study** `../3d-scenes/case-studies/<project>.md`: purpose, decision timeline table, final numbers, "what we'd do from minute one".
5. **Propose reference upgrades** (don't apply without the user's OK): which file/section changes, the new text, and why. Add rows to `09-troubleshooting.md` for every new symptom.
6. **Reusable code**: if a bpy snippet solved something twice, turn it into `scripts/<name>.py` with a CONFIG block.
7. **Privacy check before saving** (the skill is shared with friends): no IP addresses, hostnames, usernames, home paths, client or brand names, personal tokens, or machine-specific setup. Replace with generic words ("the client", "a GPU render machine", `<project>`). Run `grep -rniE "([0-9]{1,3}\.){3}[0-9]{1,3}|/Users/|C:\\\\|token|password"` over the changed files.
8. Add a line to the README changelog.
9. **Publish** (only if this copy is a git clone the user owns — `git remote get-url origin` works and they asked to keep GitHub in sync): from the repository root run `bash tools/publish.sh "<one-line note>"`. It re-checks privacy, bumps the patch version (so every installed copy sees an update), commits, pushes, and refreshes the local install. If it prints BLOCKED, remove the private text and run it again. Never push without running it.

## Where to edit
Always edit the **source repository** (the folder that has `.git` and `tools/publish.sh`), never the installed cache under `~/.claude/plugins/`. Find it with `git -C <path> remote get-url origin`.

## Quality bar for a rule
- Specific (numbers, names of settings), testable, tied to a symptom.
- Not "use good lighting" — instead "white paper hero: exclude from scene lights, own fill ≈4 W at 0.9 m".
