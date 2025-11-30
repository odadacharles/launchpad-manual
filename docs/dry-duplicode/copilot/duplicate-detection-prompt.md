# Duplicate Content Detection Prompt

You are tasked with implementing a sliding window algorithm to detect duplicate content between multiple `.rst` files across specified directories.

## Task Requirements

Scan for duplicate content between file pairs in the specified directories using the following specifications:

### Directory Scope

You can configure the script to scan different directory combinations:

1. **Sample scan** (original version): `dry-files/` subdirectory only
2. **Partial scan**: `docs/user/` and `docs/developer/` directories (recursive)
3. **Full scan**: `docs/user/`, `docs/developer/`, and `docs/dry-duplicode/` directories (recursive)
4. **Exclusions**: Always exclude `docs/includes/` directory (contains intentional reusable content)

The directories should be configurable via constants at the top of the script.

### Scanning Parameters

1. **Initial Skip**: Skip the first 140 characters of each file being scanned
2. **Window Size**: 200 characters (strict - may split words mid-character)
3. **Slide Increment**: Move forward by 1 character after each scan
4. **Match Criteria**: EXACT character-by-character matches only (case-sensitive, whitespace-sensitive)

### Algorithm

1. Start with the first file in the directory
2. Skip the initial 140 characters
3. Create a 200-character window starting at position 140
4. Check if this exact 200-character sequence exists anywhere in the second file
5. If match found:
   - Record the file pair and duplicate text
   - Stop comparing these two files (move to next file pair)
6. If no match:
   - Slide window forward by 1 character
   - Repeat until end of first file is reached
7. Once first file is compared with all other files, move to second file
8. Compare second file with third, fourth, etc. (skip comparison with first file as already done)
9. Continue until all unique file pairs have been compared

### Comparison Logic

- Each file pair should only appear in the output once
- For each new file pair, start scanning from the beginning (character 140) of the first file
- When comparing file A with file B, and a match is found, do NOT continue comparing them for additional matches
- File pairs are unique: if A vs B was compared, B vs A should not be compared again
- Files are compared across all specified directories (e.g., user files can be compared with developer files)

### File Path Display

- Display full relative paths starting from `docs/` directory for clarity
- Example: `docs/user/how-to/bug-tracking.rst` instead of just `bug-tracking.rst`
- Use a helper function to extract the path relative to the `docs/` directory

### Output Requirements

Generate a markdown report file containing:

1. **Header**: "Duplicate Content Report" (with appropriate qualifier like "Full Scan" if applicable)
2. **Scan Parameters Section**:
   - Window size: 200 characters
   - Initial skip: 140 characters
   - Directories scanned: [list of directories]
   - Files scanned: [total count with breakdown by directory]
3. **Results Section**:
   For each duplicate found, include:
   - File pair names with full relative paths from `docs/` (both files)
   - Position in first file where duplicate starts (character number)
   - The exact 200-character duplicate text in a code block
   - Separator line between duplicates

**Output file naming conventions:**
- `duplicates-report.md` for sample/dry-files scan
- `duplicates-report-full.md` for full directory scans

### Example Output Format

```markdown
# Duplicate Content Report - Full Scan

Scan parameters:
- Window size: 200 characters
- Initial skip: 140 characters
- Directories scanned: docs/user/, docs/developer/, docs/dry-duplicode/ (recursive)
- Files scanned: 310 (191 user, 115 developer, 4 dry-duplicode)

## Found 24 duplicate(s)

### Duplicate 1

**Files:**
- `docs/user/explanation/answers/answer-tracker.rst`
- `docs/dry-duplicode/dry-files/answer-tracker.rst`

**Position in first file:** Character 140

**Duplicate text:**

```
[exact 200 characters here]
```

---
```

### Implementation Details

- Work with `.rst` files only
- Use Python with pathlib for file operations
- Use `rglob("*.rst")` for recursive directory scanning
- Implement as reusable scripts with clear naming conventions:
  - `duplicate-detector.py` for sample/dry-files scans
  - `duplicate-detector-full.py` for full directory scans
- Include proper documentation and comments in code
- Handle file reading with UTF-8 encoding
- Print progress to console during execution showing:
  - Files found per directory
  - Each file pair comparison in progress
  - Success/failure indicators (✓/✗) for duplicate detection
  - Final summary statistics
- Use configuration constants for easy parameter adjustment:
  - Directory paths (USER_DIR, DEVELOPER_DIR, DRY_DUPLICODE_DIR, etc.)
  - SKIP_CHARS (default: 140)
  - WINDOW_SIZE (default: 200)
  - OUTPUT_FILE name

### Expected Deliverables

1. Python scripts with hyphenated names:
   - `duplicate-detector.py` (sample scan)
   - `duplicate-detector-full.py` (full scan)
2. Markdown reports:
   - `duplicates-report.md` (sample results)
   - `duplicates-report-full.md` (full results)
3. Console output showing:
   - Number of files found per directory
   - Total files to process
   - Comparison progress for each file pair
   - Whether duplicates were found for each pair (✓ Found duplicate at position X / ✗ No duplicates found)
   - Final summary with total duplicates found and report filename

## Notes

- The 200-character window is strict and does NOT respect word boundaries (may split words)
- Line boundaries are NOT respected (window may span multiple lines)
- Matches must be EXACT - no fuzzy matching, no normalization
- The algorithm stops at the first match for each file pair
- File naming convention: Use hyphens instead of underscores for new files
- Some files may appear in multiple duplicate pairs if they share content with different files
- The `includes/` directory should be excluded from scans as it contains intentional reusable content

## Real-World Results

When scanning the full Launchpad documentation (user/, developer/, and dry-duplicode/ directories):
- **Total files scanned**: 310 files (191 user, 115 developer, 4 dry-duplicode)
- **Duplicates found**: 24 duplicate pairs
- **Common patterns**: 
  - Test files in `dry-duplicode/dry-files/` often duplicate their source files in `user/` directories
  - Some how-to guides duplicate content from explanation pages
  - Feature highlight pages may share content with corresponding how-to guides
