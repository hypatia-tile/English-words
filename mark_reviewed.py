#!/usr/bin/env python3
"""
Mark vocabulary entries as reviewed by updating their last_reviewed timestamp.
"""

import argparse
from datetime import datetime
from pathlib import Path
from vocab_lib import load_entry, save_entry, get_all_entries, is_due_for_review


def slugify(text):
    """Convert text to a safe filename (matches add_entry.py)."""
    return text.lower().replace(' ', '-').replace('/', '-')


def find_entry_by_name(name):
    """Find an entry file by its name."""
    slug = slugify(name)

    # Check all directories
    for directory in ['words', 'idioms', 'terminologies']:
        filepath = Path(directory) / f"{slug}.yaml"
        if filepath.exists():
            return filepath

    return None


def mark_as_reviewed(filepath):
    """Update the last_reviewed timestamp for an entry."""
    entry = load_entry(filepath)
    entry['last_reviewed'] = datetime.now().isoformat()
    save_entry(filepath, entry)
    return entry


def main():
    parser = argparse.ArgumentParser(
        description='Mark vocabulary entries as reviewed',
        epilog='If no entry names are provided, all entries due for review will be marked.'
    )
    parser.add_argument('names', nargs='*', help='Names of entries to mark as reviewed')
    parser.add_argument('--days', type=int, default=7,
                        help='Number of days before an entry is due for review (default: 7)')

    args = parser.parse_args()

    if args.names:
        # Mark specific entries
        marked = []
        not_found = []

        for name in args.names:
            filepath = find_entry_by_name(name)
            if filepath:
                entry = mark_as_reviewed(filepath)
                marked.append((filepath, entry['name']))
                print(f"Marked as reviewed: {entry['name']} ({filepath})")
            else:
                not_found.append(name)
                print(f"Warning: Entry not found: {name}")

        if marked:
            print(f"\nSuccessfully marked {len(marked)} entries as reviewed.")
        if not_found:
            print(f"\nCould not find {len(not_found)} entries.")

    else:
        # Mark all entries due for review
        entry_files = get_all_entries()
        due_entries = []

        for filepath in entry_files:
            try:
                entry = load_entry(filepath)
                if is_due_for_review(entry, args.days):
                    due_entries.append(filepath)
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")

        if not due_entries:
            print(f"No entries are due for review (checked with {args.days}-day interval).")
            return 0

        print(f"Found {len(due_entries)} entries due for review.")
        print("Marking all as reviewed...\n")

        marked = []
        for filepath in due_entries:
            entry = mark_as_reviewed(filepath)
            marked.append(entry['name'])
            print(f"  ✓ {entry['name']}")

        print(f"\nSuccessfully marked {len(marked)} entries as reviewed.")
        print("\nYou can now commit these changes to GitHub:")
        print(f"  git add .")
        print(f'  git commit -m "Review: marked {len(marked)} entries as reviewed"')
        print(f"  git push")

    return 0


if __name__ == '__main__':
    exit(main())
