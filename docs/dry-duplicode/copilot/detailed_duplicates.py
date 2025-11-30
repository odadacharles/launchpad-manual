#!/usr/bin/env python3
"""
Find and categorize duplicated content in .rst files.
"""
import os
import re
from collections import defaultdict

def clean_text(text):
    """Remove extra whitespace and normalize text."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_file_location(filepath, text_to_find, original_content):
    """Find approximate line number of text in file."""
    lines = original_content.split('\n')
    # Try to find a distinctive part
    search_text = text_to_find[:100].strip()
    for i, line in enumerate(lines, 1):
        if search_text[:50] in line or line in search_text:
            return f"around line {i}"
    return "location unknown"

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
    file_contents = {}
    
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
                        file_contents[filepath] = content
                except Exception as e:
                    pass
    
    print(f"Analyzing {len(rst_files)} .rst files (excluding build/venv dirs)")
    
    # Build a map of text segments to files
    segment_map = defaultdict(list)
    
    for filepath, content in rst_files.items():
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            cleaned = clean_text(para)
            if len(cleaned) >= min_duplicate_length:
                key = cleaned[:150]
                segment_map[key].append((filepath, cleaned, para))
    
    # Find actual duplicates
    duplicates = []
    
    for key, instances in segment_map.items():
        if len(instances) > 1:
            files_with_content = {}
            for filepath, cleaned, original in instances:
                if cleaned not in files_with_content:
                    files_with_content[cleaned] = []
                files_with_content[cleaned].append((filepath, original))
            
            for cleaned_text, file_list in files_with_content.items():
                if len(file_list) > 1:
                    duplicates.append({
                        'text': cleaned_text,
                        'originals': {f: orig for f, orig in file_list},
                        'files': [f for f, _ in file_list],
                        'length': len(cleaned_text),
                        'category': categorize_content(cleaned_text)
                    })
    
    duplicates.sort(key=lambda x: x['length'], reverse=True)
    
    # Remove duplicates in the duplicates list
    seen = set()
    unique_duplicates = []
    for dup in duplicates:
        files_key = tuple(sorted(dup['files']))
        text_key = dup['text'][:100]
        combo_key = (files_key, text_key)
        if combo_key not in seen:
            seen.add(combo_key)
            unique_duplicates.append(dup)
    
    return unique_duplicates, file_contents

def main():
    docs_dir = '/home/charles.odada@canonical.com/Documents/Work Repos/launchpad-manual/docs'
    
    duplicates, file_contents = find_duplicates(docs_dir, min_duplicate_length=200)
    
    # Categorize by content type
    by_category = defaultdict(list)
    for dup in duplicates:
        by_category[dup['category']].append(dup)
    
    print(f"\n{'='*80}")
    print(f"DUPLICATE CONTENT ANALYSIS REPORT")
    print(f"{'='*80}")
    print(f"\nTotal substantial duplicates found: {len(duplicates)}")
    print(f"\nBreakdown by category:")
    for cat, dups in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  - {cat}: {len(dups)} duplicates")
    
    print(f"\n{'='*80}")
    print("DETAILED DUPLICATE FINDINGS")
    print(f"{'='*80}\n")
    
    for i, dup in enumerate(duplicates[:30], 1):  # Show top 30
        print(f"### DUPLICATE #{i}")
        print(f"Content Type: {dup['category']}")
        print(f"Character Count: {dup['length']} characters")
        print(f"Number of Files: {len(dup['files'])}")
        print(f"\nFiles containing this duplicate:")
        
        for filepath in dup['files']:
            rel_path = filepath.replace(docs_dir + '/', '')
            original = dup['originals'][filepath]
            location = get_file_location(filepath, dup['text'], file_contents[filepath])
            print(f"  • {rel_path}")
            print(f"    Location: {location}")
        
        # Show text excerpt
        excerpt = dup['text'][:250]
        if len(dup['text']) > 250:
            excerpt += "..."
        print(f"\nText Excerpt (first 250 chars):")
        print(f"{excerpt}")
        print(f"\n{'-'*80}\n")

if __name__ == '__main__':
    main()
