#!/usr/bin/env python3
"""
Duplicate Content Detector using Sliding Window Algorithm

This script scans .rst files in the dry-files directory to find duplicate
content between file pairs using a sliding window approach.

Configuration:
- Window size: 200 characters (strict)
- Initial skip: 140 characters from start of each file
- Slide increment: 1 character per iteration
- Match criteria: Exact character sequence match

Output:
- Generates duplicates-report.md with all found duplicates
"""

import os
from pathlib import Path

# Configuration
DRY_FILES_DIR = Path("dry-files")
SKIP_CHARS = 140
WINDOW_SIZE = 200
OUTPUT_FILE = "duplicates-report.md"

def read_file_content(filepath):
    """Read file content as string."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def find_duplicate(text1, text2, skip_chars, window_size):
    """
    Find first duplicate between two texts using sliding window.
    
    Args:
        text1: Content of first file
        text2: Content of second file
        skip_chars: Number of characters to skip from start of text1
        window_size: Size of the sliding window in characters
    
    Returns:
        tuple (position, duplicate_text) or None if no match found
    """
    # Start from skip_chars position in text1
    for i in range(skip_chars, len(text1) - window_size + 1):
        window = text1[i:i + window_size]
        # Check if this exact window exists anywhere in text2
        if window in text2:
            return (i, window)
    return None

def main():
    # Get all .rst files in dry-files directory
    files = sorted([f for f in DRY_FILES_DIR.glob("*.rst")])
    print(f"Found {len(files)} files to process")
    
    # Track which pairs have been compared
    compared_pairs = set()
    duplicates = []
    
    # Compare each file with every other file
    for i, file1 in enumerate(files):
        for file2 in files[i+1:]:
            pair_key = (file1.name, file2.name)
            
            if pair_key in compared_pairs:
                continue
            
            print(f"Comparing {file1.name} with {file2.name}...")
            
            # Read both files
            content1 = read_file_content(file1)
            content2 = read_file_content(file2)
            
            # Find duplicate
            result = find_duplicate(content1, content2, SKIP_CHARS, WINDOW_SIZE)
            
            if result:
                position, duplicate_text = result
                duplicates.append({
                    'file1': file1.name,
                    'file2': file2.name,
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
        f.write("# Duplicate Content Report\n\n")
        f.write(f"Scan parameters:\n")
        f.write(f"- Window size: {WINDOW_SIZE} characters\n")
        f.write(f"- Initial skip: {SKIP_CHARS} characters\n")
        f.write(f"- Files scanned: {len(files)}\n\n")
        
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
