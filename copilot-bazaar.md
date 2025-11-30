# Bazaar Reference Identification Prompt

You are analyzing documentation in a Launchpad manual repository to identify all references to Bazaar, the legacy version control system that Launchpad has largely replaced with Git.

## Task
Scan documentation files (primarily `.rst` format) to identify any references to Bazaar-related terminology, commands, workflows, or infrastructure that may need updating or removal as part of modernizing the documentation for Git-based workflows.

## What to Look For

### Direct References
- "Bazaar" or "bazaar" (the VCS name)
- "bzr" (Bazaar command-line tool)
- "Breezy" or "breezy" (actively maintained Bazaar fork)
- "brz" (Breezy command-line tool)

### Commands and Syntax
- `bzr branch`, `bzr commit`, `bzr push`, `bzr merge`, etc.
- `brz` commands (Breezy equivalents)
- `lp:projectname` notation (Bazaar-specific URL scheme for Launchpad)
- `bzr+ssh://` protocol references

### URLs and Hostnames
- `bazaar.launchpad.net` (production Bazaar hosting)
- `bazaar.launchpad.test` (development/test Bazaar vhost)
- `bazaar-internal.launchpad.test`

### Directory and File References
- `brzplugins/` directory
- `.bzr/` directories or configuration
- `.bzrignore` files

### Terminology Differences (Bazaar vs Git)
- **trunk** - Bazaar's default branch name (Git uses "main" or "master")
- **revision numbers** - sequential numbers like "r123" (Git uses commit hashes)
- **merge directives** - Bazaar's patch/merge format (Git uses pull requests/patches)
- **bound branches** - Bazaar concept (Git uses tracking branches differently)
- **checkout vs branch** - Bazaar distinguishes these concepts differently than Git
- **nick** - branch nickname in Bazaar
- **shelve** - Bazaar term for temporarily setting aside changes (Git uses "stash")
- **loggerhead** - Bazaar web code viewer (replaced by cgit for Git)

### Workflows and Concepts
- Branch-per-developer publish/pull patterns specific to Bazaar
- "Request Bazaar Import" UI actions or pages
- Bazaar-specific merge algorithms or conflict resolution
- File ID tracking (explicit in Bazaar, heuristic in Git)
- Bazaar smart server references

### Configuration Examples
- SSH config blocks for `Host bazaar.launchpad.net`
- Apache vhost configurations for Bazaar services
- `/etc/hosts` entries for `bazaar.launchpad.test` domains

## Exceptions and Context

### When NOT to Flag
- References that are clearly historical or in legacy/archive sections appropriately marked
- Infrastructure that legitimately still uses Breezy/brz if Launchpad hasn't fully migrated
- Comparative documentation explicitly contrasting Bazaar and Git workflows

### Ambiguous Cases
- `brzplugins/` directory: May still be actively used infrastructure - verify before flagging for removal
- "trunk" in project series context: May be a legitimate series name even in Git context, but flag for review
- Code import references: Verify whether Bazaar imports are still supported vs deprecated

## Output Format

For each file scanned, report:

1. **File path** (relative to repository root)
2. **Line number(s)** where references occur
3. **Type of reference** (direct mention, command, URL, terminology, etc.)
4. **Exact text or context** (quote the relevant line or section)
5. **Recommendation**: 
   - Remove (clearly obsolete)
   - Update to Git equivalent (needs modernization)
   - Review (may still be valid infrastructure)
   - Historical (appropriate in context)

## Example Output

```
File: docs/user/explanation/what-is-launchpad.rst
Line: 64
Type: Direct command reference
Text: "If you want to use Launchpad and bzr for your free software project"
Recommendation: Update - change "bzr" to "Git"

File: docs/developer/how-to/running.rst
Lines: 165-166
Type: SSH configuration
Text: "Host bazaar.launchpad.net\n    User LPUSERNAME"
Recommendation: Remove - replaced by git.launchpad.net configuration

File: docs/developer/explanation/navigating.rst
Lines: 59-60
Type: Directory reference
Text: "brzplugins/\n    Breezy plugins used in running Launchpad."
Recommendation: Review - verify if Breezy plugins still actively used
```

## Execution Strategy

1. Prioritize scanning `.rst` files in `docs/user/` and `docs/developer/` directories
2. Use case-insensitive pattern matching for text searches
3. Check both inline text and code blocks
4. Verify context around matches to avoid false positives
5. Cross-reference with Git equivalents to ensure complete coverage

## Goal

Produce a comprehensive audit of all Bazaar-related references to support the modernization of Launchpad documentation for a Git-first workflow, while preserving legitimately required legacy infrastructure documentation.
