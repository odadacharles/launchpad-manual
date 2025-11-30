#!/usr/bin/env python3
"""
Find duplicated content in .rst files.
"""
import os
import re
from collections import defaultdict
from difflib import SequenceMatcher

def clean_text(text):
    """Remove extra whitespace and normalize text."""
    # Remove RST directives and references for cleaner comparison
    text = re.sub(r'\.\. \w+::', '', text)
    text = re.sub(r':ref:`[^`]+`', '', text)
    text = re.sub(r':doc:`[^`]+`', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_text_chunks(text, min_length=100):
    """Split text into overlapping chunks for comparison."""
    words = text.split()
    chunks = []
    chunk_size = 50  # words per chunk
    overlap = 25     # words overlap
    
    for i in range(0, len(words) - chunk_size + 1, chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk) >= min_length:
            chunks.append((i, chunk))
    return chunks

def find_duplicates(docs_dir, min_duplicate_length=200):
    """Find duplicated content across .rst files."""
    
    # Read all .rst files
    rst_files = {}
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.rst'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        rst_files[filepath] = content
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    print(f"Found {len(rst_files)} .rst files")
    
    # Build a map of text segments to files
    segment_map = defaultdict(list)
    
    for filepath, content in rst_files.items():
        # Clean and split into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            cleaned = clean_text(para)
            if len(cleaned) >= min_duplicate_length:
                # Use first 150 chars as key for grouping
                key = cleaned[:150]
                segment_map[key].append((filepath, cleaned, para))
    
    # Find actual duplicates
    duplicates = []
    
    for key, instances in segment_map.items():
        if len(instances) > 1:
            # Check if these are truly similar
            files_with_content = {}
            for filepath, cleaned, original in instances:
                if cleaned not in files_with_content:
                    files_with_content[cleaned] = []
                files_with_content[cleaned].append((filepath, original))
            
            for cleaned_text, file_list in files_with_content.items():
                if len(file_list) > 1:
                    duplicates.append({
                        'text': cleaned_text,
                        'original': file_list[0][1],
                        'files': [f[0] for f in file_list],
                        'length': len(cleaned_text)
                    })
    
    # Sort by length (most substantial first)
    duplicates.sort(key=lambda x: x['length'], reverse=True)
    
    # Remove duplicates in the duplicates list itself
    seen = set()
    unique_duplicates = []
    for dup in duplicates:
        files_key = tuple(sorted(dup['files']))
        text_key = dup['text'][:100]
        combo_key = (files_key, text_key)
        if combo_key not in seen:
            seen.add(combo_key)
            unique_duplicates.append(dup)
    
    return unique_duplicates

def main():
    docs_dir = '/home/charles.odada@canonical.com/Documents/Work Repos/launchpad-manual/docs'
    
    print("Searching for duplicates in .rst files...")
    print("=" * 80)
    
    duplicates = find_duplicates(docs_dir, min_duplicate_length=200)
    
    print(f"\nFound {len(duplicates)} substantial duplicates\n")
    print("=" * 80)
    
    for i, dup in enumerate(duplicates[:50], 1):  # Show top 50
        print(f"\n### Duplicate #{i}")
        print(f"Character count: {dup['length']}")
        print(f"Found in {len(dup['files'])} files:")
        for filepath in dup['files']:
            rel_path = filepath.replace(docs_dir + '/', '')
            print(f"  - {rel_path}")
        
        # Show excerpt
        excerpt = dup['text'][:200]
        if len(dup['text']) > 200:
            excerpt += "..."
        print(f"\nText excerpt:\n{excerpt}")
        print("-" * 80)

if __name__ == '__main__':
    main()
