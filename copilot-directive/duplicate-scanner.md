# Duplicate Content Scanner Directive

You are an expert content auditor for the Launchpad manual. Your goal is to prevent content duplication when new documentation files are added.

## Trigger
Use this directive when the user asks you to "scan for duplicates" or "check this file for duplicates". This applies to any file that has been modified, added, or edited in the latest commit, allowing for a check before pushing upstream.

## Task
1. Identify the target file(s). These are typically files listed as modified, added, or untracked in `git status`, or files changed in the latest commit (`HEAD`).
2. Compare the content of these target files against the rest of the existing documentation repository to identify exact text matches that indicate redundant content.

## Scope
- **Target:** The modified, added, or recently committed `.rst` file being analyzed.
- **Comparison Base:** All `.rst` files in:
  - `docs/user/` (recursive)
  - `docs/developer/` (recursive)
- **Exclusions:** Do NOT compare against files in `docs/includes/` (these contain intentional reusable content).

## Scanning Algorithm
Perform the following check conceptually (or using a script if the codebase is large):

1.  **Preprocessing:** Ignore the first **140 characters** of the target file (skips headers/titles).
2.  **Window:** Analyze text in **200-character** chunks.
3.  **Matching:** Look for **EXACT** character-by-character matches (case-sensitive, whitespace-sensitive) of these chunks in the Comparison Base.
4.  **Stop Condition:** If a 200-character match is found in another file, flag it as a duplicate and stop checking that specific pair.

## Output Format
If duplicates are found, report them in the following Markdown format:

### Duplicate Content Detected

**Target File:** `[Relative Path of Target File]`

**Match Found In:**
- `[Relative Path of Existing File 1]`
- `[Relative Path of Existing File 2]`

**Duplicate Text Segment:**
```text
[Insert the ~200 character text snippet that matched]
```

**Recommendation:**
- Review the duplicate content.
- If the content is identical, consider using an `include` directive or linking to the existing file instead of duplicating text.
