# GitHub Copilot Instructions for Launchpad Manual

## Duplicate Content Detection

When reviewing changes to documentation files in the `docs/` directory, automatically check for content duplication.

### When to Check
- When files are added or modified in `docs/user/` or `docs/developer/`
- Before committing changes to `.rst` files
- When the user requests a duplicate check

### Scanning Process

1. **Identify Target Files:**
   - Files shown as modified, added, or untracked in `git status`
   - Files changed in the latest commit
   - Focus on `.rst` files

2. **Compare Against:**
   - All `.rst` files in `docs/user/` (recursive)
   - All `.rst` files in `docs/developer/` (recursive)
   - **Exclude:** Files in `docs/includes/` (intentional reusable content)

3. **Detection Algorithm:**
   - Skip the first 140 characters of the target file (headers/titles)
   - Analyze text in 200-character chunks
   - Look for exact character-by-character matches (case-sensitive, whitespace-sensitive)
   - Flag matches as potential duplicates

### Reporting Duplicates

If duplicate content is detected, report it as:

```markdown
### Duplicate Content Detected

**Target File:** `path/to/target/file.rst`

**Match Found In:**
- `path/to/existing/file1.rst`
- `path/to/existing/file2.rst`

**Duplicate Text Segment:**
```text
[The ~200 character text snippet that matched]
```

**Recommendation:**
- Review the duplicate content
- Consider using an `include` directive or linking to the existing file
- Avoid duplicating text that already exists elsewhere in the documentation
```

### Best Practices
- If content needs to appear in multiple places, use reStructuredText `include` directives
- Reference existing documentation with links rather than duplicating explanations
- Keep content DRY (Don't Repeat Yourself)
