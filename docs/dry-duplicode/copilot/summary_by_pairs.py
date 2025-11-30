#!/usr/bin/env python3
"""
Comprehensive duplicate analysis grouped by file pairs.
"""
import os
import re
from collections import defaultdict

def clean_text(text):
    """Remove extra whitespace and normalize text."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def categorize_content(text):
    """Categorize the type of content."""
    text_lower = text.lower()
    
    if 'http://' in text or 'https://' in text:
        if 'api' in text_lower:
            return "API documentation"
        elif 'git' in text_lower or 'bzr' in text_lower or 'repository' in text_lower:
            return "Version control instructions"
    
    if any(word in text_lower for word in ['install', 'setup', 'configure', 'run']):
        return "Setup/Installation instructions"
    
    if any(word in text_lower for word in ['click', 'select', 'navigate', 'follow']):
        return "UI/Procedure instructions"
    
    if any(word in text_lower for word in ['copyright', 'license', 'trademark']):
        return "Legal/License text"
    
    if any(word in text_lower for word in ['example', 'for instance', 'such as']):
        return "Examples/Explanations"
    
    return "General documentation"

def find_duplicates(docs_dir, min_duplicate_length=200):
    """Find duplicated content across .rst files."""
    
    rst_files = {}
    
    for root, dirs, files in os.walk(docs_dir):
        # Skip virtual environment and build directories
        if '.sphinx' in root or '_build' in root or '__pycache__' in root:
            continue
            
        for file in files:
            if file.endswith('.rst'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        rst_files[filepath] = content
                except Exception as e:
                    pass
    
    print(f"Analyzing {len(rst_files)} .rst files")
    
    # Build a map of text segments to files
    segment_map = defaultdict(list)
    
    for filepath, content in rst_files.items():
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            cleaned = clean_text(para)
            if len(cleaned) >= min_duplicate_length:
                key = cleaned[:150]
                segment_map[key].append((filepath, cleaned, para))
    
    # Find actual duplicates and group by file pairs
    file_pair_duplicates = defaultdict(list)
    
    for key, instances in segment_map.items():
        if len(instances) > 1:
            files_with_content = {}
            for filepath, cleaned, original in instances:
                if cleaned not in files_with_content:
                    files_with_content[cleaned] = []
                files_with_content[cleaned].append((filepath, original))
            
            for cleaned_text, file_list in files_with_content.items():
                if len(file_list) > 1:
                    files = tuple(sorted([f for f, _ in file_list]))
                    file_pair_duplicates[files].append({
                        'text': cleaned_text,
                        'length': len(cleaned_text),
                        'category': categorize_content(cleaned_text)
                    })
    
    return file_pair_duplicates, rst_files

def main():
    docs_dir = '/home/charles.odada@canonical.com/Documents/Work Repos/launchpad-manual/docs'
    
    file_pair_duplicates, rst_files = find_duplicates(docs_dir, min_duplicate_length=200)
    
    # Calculate total duplications
    total_duplicates = sum(len(dups) for dups in file_pair_duplicates.values())
    
    print(f"\n{'='*80}")
    print(f"DUPLICATE CONTENT SUMMARY BY FILE PAIRS")
    print(f"{'='*80}")
    print(f"\nTotal file pairs with duplicates: {len(file_pair_duplicates)}")
    print(f"Total duplicate segments found: {total_duplicates}")
    
    # Sort by number of duplicates between pairs
    sorted_pairs = sorted(file_pair_duplicates.items(), 
                         key=lambda x: (len(x[1]), sum(d['length'] for d in x[1])),
                         reverse=True)
    
    print(f"\n{'='*80}")
    print("DETAILED FILE PAIR ANALYSIS")
    print(f"{'='*80}\n")
    
    for i, (files, duplicates) in enumerate(sorted_pairs, 1):
        total_chars = sum(d['length'] for d in duplicates)
        
        print(f"### FILE PAIR #{i}")
        print(f"Number of duplicate segments: {len(duplicates)}")
        print(f"Total duplicate characters: {total_chars}")
        print(f"\nFiles involved:")
        for filepath in files:
            rel_path = filepath.replace(docs_dir + '/', '')
            print(f"  • {rel_path}")
        
        # Categorize duplicates
        by_category = defaultdict(list)
        for dup in duplicates:
            by_category[dup['category']].append(dup)
        
        print(f"\nContent breakdown:")
        for cat, dups in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
            total_cat_chars = sum(d['length'] for d in dups)
            print(f"  - {cat}: {len(dups)} segments ({total_cat_chars} chars)")
        
        # Show largest duplicate
        largest = max(duplicates, key=lambda x: x['length'])
        excerpt = largest['text'][:200]
        if len(largest['text']) > 200:
            excerpt += "..."
        print(f"\nLargest duplicate ({largest['length']} chars):")
        print(f"{excerpt}")
        
        print(f"\n{'-'*80}\n")

if __name__ == '__main__':
    main()
