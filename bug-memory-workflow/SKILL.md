---
name: bug-memory-workflow
description: Use when fixing, debugging, investigating, or reviewing any bug, regression, failing test, runtime error, UI defect, API defect, Feishu bug, or user-reported problem where prior bug history may prevent repeated mistakes.
---

# Bug Memory Workflow

## Overview

Use this skill as the memory gate around bug work. Read relevant historical bug memories before changing code, then record one compact bug memory after the fix is verified.

**REQUIRED SUB-SKILLS:** Use `superpowers:systematic-debugging` for diagnosis and `superpowers:verification-before-completion` before claiming the bug is fixed.

## Workflow

1. Extract search terms from the bug report: repo name, package, route/page, component, API, error text, data key, visible symptom, and touched files.
2. Search historical bug memories before editing code. Read `references/bug-memory-notes.md` for paths, search commands, and note format.
3. Summarize only relevant prior memories before debugging: symptom, root cause, fix, and reuse hint. If none are found, say none were found and continue.
4. Diagnose and fix the bug using normal repo workflow and any repo-specific skills or memories.
5. Verify the original symptom or failing test with fresh evidence.
6. After verification, write one compact bug memory note automatically unless the user explicitly says not to record memory.

## Hard Rules

- Do not edit code before the historical memory search is complete.
- Do not record guesses as memory. Store confirmed facts only.
- Do not write a bug memory for abandoned, unverified, or unresolved work. Instead, tell the user what is missing.
- Keep each memory note small and searchable.
- Keep repo-specific delivery rules separate. For example, `bug-des` still handles bug-description output when requested.

## Common Mistakes

- Skipping memory search because the bug looks simple: still search first.
- Writing a note with "probably" root causes: omit uncertain claims.
- Recording huge diffs or full narratives: store the reusable lesson, not the whole session.
- Letting memory capture replace verification: verification remains mandatory.
