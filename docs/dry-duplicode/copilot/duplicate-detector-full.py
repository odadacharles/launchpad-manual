"""
Duplicate Content Detector - Full Scan Version

Scans all .rst files in docs/user/, docs/developer/, and docs/dry-duplicode/ directories recursively
to detect duplicate content using a sliding window algorithm.
Excludes the includes/ directory.
"""

import os
from pathlib import Path

# Configuration
USER_DIR = Path("../../user")
DEVELOPER_DIR = Path("../../developer")
DRY_DUPLICODE_DIR = Path("..")
SKIP_CHARS = 140
WINDOW_SIZE = 200
OUTPUT_FILE = "duplicates-report-full.md"

def read_file_content(filepath):
    """Read file content as string."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def find_duplicate(text1, text2, skip_chars, window_size):
    """
    Find first duplicate between two texts using sliding window.
    Returns tuple (position, duplicate_text) or None if no match.
    """
    # Start from skip_chars position in text1
    for i in range(skip_chars, len(text1) - window_size + 1):
        window = text1[i:i + window_size]
        # Check if this exact window exists anywhere in text2
        if window in text2:
            return (i, window)
    return None

def get_relative_path(filepath):
    """Get path relative to docs/ directory for display."""
    # Convert to absolute path first
    abs_path = filepath.resolve()
    # Find the 'docs' directory in the path
    parts = abs_path.parts
    try:
        docs_index = parts.index('docs')
        # Return path from docs/ onwards
        return str(Path(*parts[docs_index:]))
    except ValueError:
        # If 'docs' not found, return the filename
        return filepath.name

def main():
    # Get all .rst files from all three directories recursively
    user_files = sorted(USER_DIR.rglob("*.rst"))
    developer_files = sorted(DEVELOPER_DIR.rglob("*.rst"))
    dry_duplicode_files = sorted(DRY_DUPLICODE_DIR.rglob("*.rst"))
    
    # Combine all files
    all_files = user_files + developer_files + dry_duplicode_files
    
    print(f"Found {len(user_files)} files in user/ directory")
    print(f"Found {len(developer_files)} files in developer/ directory")
    print(f"Found {len(dry_duplicode_files)} files in dry-duplicode/ directory")
    print(f"Total: {len(all_files)} files to process\n")

    # Track which pairs have been compared
    compared_pairs = set()
    duplicates = []

    # Compare each file with every other file
    for i, file1 in enumerate(all_files):
        for file2 in all_files[i+1:]:
            # Use full paths as keys to ensure uniqueness
            pair_key = (str(file1), str(file2))

            if pair_key in compared_pairs:
                continue

            rel_path1 = get_relative_path(file1)
            rel_path2 = get_relative_path(file2)
            
            print(f"Comparing {rel_path1} with {rel_path2}...")

            # Read both files
            content1 = read_file_content(file1)
            content2 = read_file_content(file2)

            # Find duplicate
            result = find_duplicate(content1, content2, SKIP_CHARS, WINDOW_SIZE)

            if result:
                position, duplicate_text = result
                duplicates.append({
                    'file1': rel_path1,
                    'file2': rel_path2,
                    'position': position,
                    'text': duplicate_text
                })
                print(f"  ✓ Found duplicate at position {position}")
                # Mark this pair as compared and move to next file2
                compared_pairs.add(pair_key)
                break  # Move to next file1 vs remaining files
            else:
                print(f"  ✗ No duplicates found")

            compared_pairs.add(pair_key)

    # Write results to markdown file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Duplicate Content Report - Full Scan\n\n")
        f.write(f"Scan parameters:\n")
        f.write(f"- Window size: {WINDOW_SIZE} characters\n")
        f.write(f"- Initial skip: {SKIP_CHARS} characters\n")
        f.write(f"- Directories scanned: docs/user/, docs/developer/, docs/dry-duplicode/ (recursive)\n")
        f.write(f"- Files scanned: {len(all_files)} ({len(user_files)} user, {len(developer_files)} developer, {len(dry_duplicode_files)} dry-duplicode)\n\n")

        if duplicates:
            f.write(f"## Found {len(duplicates)} duplicate(s)\n\n")
            for idx, dup in enumerate(duplicates, 1):
                f.write(f"### Duplicate {idx}\n\n")
                f.write(f"**Files:**\n")
                f.write(f"- `{dup['file1']}`\n")
                f.write(f"- `{dup['file2']}`\n\n")
                f.write(f"**Position in first file:** Character {dup['position']}\n\n")
                f.write(f"**Duplicate text:**\n\n")
                f.write("```\n")
                f.write(dup['text'])
                f.write("\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("## No duplicates found\n\n")
            f.write("No exact 200-character matches were found between any file pairs.\n")

    print(f"\n✓ Report written to {OUTPUT_FILE}")
    print(f"  Total duplicates found: {len(duplicates)}")

if __name__ == "__main__":
    main()
