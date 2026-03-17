#!/usr/bin/env python3
"""
Analyze codebase structure and identify cleanup opportunities.
Outputs a report of file dependencies, unused files, and cleanup recommendations.
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List

IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__', '.next', 'dist', 'build', 
    'venv', '.venv', 'env', '.env', 'coverage', '.nyc_output', '.cache',
    '.idea', '.vscode', 'vendor', 'target'
}

JUNK_FILES = {
    '.DS_Store', 'Thumbs.db', 'desktop.ini', '.gitkeep', '.keep'
}

JUNK_PATTERNS = [
    r'.*\.pyc$', r'.*\.pyo$', r'.*\.swp$', r'.*\.swo$', 
    r'.*~$', r'.*\.bak$', r'.*\.backup$', r'.*\.log$',
    r'.*\.orig$', r'.*\.tmp$'
]

CODE_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte',
    '.rb', '.go', '.rs', '.java', '.kt', '.swift', '.c', '.cpp', '.h'
}


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored."""
    parts = path.parts
    return any(part in IGNORE_DIRS for part in parts)


def is_junk_file(filename: str) -> bool:
    """Check if file is junk."""
    if filename in JUNK_FILES:
        return True
    return any(re.match(p, filename) for p in JUNK_PATTERNS)


def extract_imports_js(content: str) -> Set[str]:
    """Extract imports from JS/TS files."""
    imports = set()
    patterns = [
        r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
        r'import\s+[\'"](.+?)[\'"]',
        r'require\s*\(\s*[\'"](.+?)[\'"]\s*\)',
        r'import\s*\(\s*[\'"](.+?)[\'"]\s*\)',
    ]
    for pattern in patterns:
        imports.update(re.findall(pattern, content))
    return imports


def extract_imports_py(content: str) -> Set[str]:
    """Extract imports from Python files."""
    imports = set()
    patterns = [
        r'^import\s+(\S+)',
        r'^from\s+(\S+)\s+import',
    ]
    for pattern in patterns:
        imports.update(re.findall(pattern, content, re.MULTILINE))
    return imports


def resolve_import(import_path: str, source_file: Path, root: Path) -> Path | None:
    """Try to resolve an import to a file path."""
    if import_path.startswith('.'):
        base = source_file.parent
        parts = import_path.split('/')
        for part in parts:
            if part == '.':
                continue
            elif part == '..':
                base = base.parent
            else:
                base = base / part
        
        for ext in ['', '.ts', '.tsx', '.js', '.jsx', '.py', '/index.ts', '/index.tsx', '/index.js']:
            candidate = base.with_suffix(ext) if ext.startswith('.') else Path(str(base) + ext)
            if candidate.exists():
                return candidate
    return None


def analyze_directory(root: Path) -> Dict:
    """Analyze a directory and return cleanup report."""
    report = {
        'total_files': 0,
        'code_files': 0,
        'junk_files': [],
        'empty_dirs': [],
        'large_dirs': [],
        'potentially_unused': [],
        'file_tree': defaultdict(list),
        'imports_graph': defaultdict(set),
        'imported_by': defaultdict(set),
    }
    
    all_code_files = set()
    
    for dirpath, dirnames, filenames in os.walk(root):
        path = Path(dirpath)
        
        if should_ignore(path):
            dirnames.clear()
            continue
        
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        if not filenames and not dirnames:
            rel_path = path.relative_to(root)
            report['empty_dirs'].append(str(rel_path))
            continue
        
        if len(filenames) > 20:
            rel_path = path.relative_to(root)
            report['large_dirs'].append({
                'path': str(rel_path),
                'file_count': len(filenames)
            })
        
        for filename in filenames:
            report['total_files'] += 1
            file_path = path / filename
            rel_path = file_path.relative_to(root)
            
            if is_junk_file(filename):
                report['junk_files'].append(str(rel_path))
                continue
            
            ext = file_path.suffix.lower()
            if ext in CODE_EXTENSIONS:
                report['code_files'] += 1
                all_code_files.add(str(rel_path))
                
                try:
                    content = file_path.read_text(errors='ignore')
                    
                    if ext in {'.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte'}:
                        imports = extract_imports_js(content)
                    elif ext == '.py':
                        imports = extract_imports_py(content)
                    else:
                        imports = set()
                    
                    for imp in imports:
                        resolved = resolve_import(imp, file_path, root)
                        if resolved:
                            resolved_rel = str(resolved.relative_to(root))
                            report['imports_graph'][str(rel_path)].add(resolved_rel)
                            report['imported_by'][resolved_rel].add(str(rel_path))
                except Exception:
                    pass
            
            parent_dir = str(path.relative_to(root))
            report['file_tree'][parent_dir].append(filename)
    
    for code_file in all_code_files:
        is_entry = any(p in code_file.lower() for p in ['index.', 'main.', 'app.', 'server.', '__init__'])
        is_test = any(p in code_file.lower() for p in ['test', 'spec', '__test__', '.test.', '.spec.'])
        is_config = any(p in code_file.lower() for p in ['config', 'settings', '.d.ts'])
        
        if not is_entry and not is_test and not is_config:
            if code_file not in report['imported_by']:
                report['potentially_unused'].append(code_file)
    
    report['imports_graph'] = {k: list(v) for k, v in report['imports_graph'].items()}
    report['imported_by'] = {k: list(v) for k, v in report['imported_by'].items()}
    
    return report


def print_report(report: Dict):
    """Print a human-readable report."""
    print("=" * 60)
    print("CODEBASE ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"\n## Overview")
    print(f"Total files: {report['total_files']}")
    print(f"Code files: {report['code_files']}")
    
    if report['junk_files']:
        print(f"\n## Junk Files ({len(report['junk_files'])} files)")
        print("Safe to delete:")
        for f in report['junk_files'][:20]:
            print(f"  - {f}")
        if len(report['junk_files']) > 20:
            print(f"  ... and {len(report['junk_files']) - 20} more")
    
    if report['empty_dirs']:
        print(f"\n## Empty Directories ({len(report['empty_dirs'])})")
        print("Safe to delete:")
        for d in report['empty_dirs'][:10]:
            print(f"  - {d}/")
        if len(report['empty_dirs']) > 10:
            print(f"  ... and {len(report['empty_dirs']) - 10} more")
    
    if report['large_dirs']:
        print(f"\n## Large Directories (>20 files)")
        print("Consider splitting:")
        for d in report['large_dirs']:
            print(f"  - {d['path']}/ ({d['file_count']} files)")
    
    if report['potentially_unused']:
        print(f"\n## Potentially Unused Files ({len(report['potentially_unused'])})")
        print("Verify before removing (may be dynamically imported):")
        for f in report['potentially_unused'][:20]:
            print(f"  - {f}")
        if len(report['potentially_unused']) > 20:
            print(f"  ... and {len(report['potentially_unused']) - 20} more")
    
    print("\n" + "=" * 60)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    if not root.exists():
        print(f"Error: {root} does not exist")
        sys.exit(1)
    
    report = analyze_directory(root)
    print_report(report)
    
    json_path = root / 'cleanup_report.json'
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\nDetailed report saved to: {json_path}")


if __name__ == '__main__':
    main()
