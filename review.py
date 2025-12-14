#!/usr/bin/env python3
"""
Show vocabulary entries due for review today.
"""

import argparse
from vocab_lib import load_entry, get_all_entries, is_due_for_review, get_entry_status


def display_entry(filepath, entry, index, total):
    """Display a single entry for review."""
    print(f"\n{'='*60}")
    print(f"Entry {index}/{total}: {entry['name']}")
    print(f"File: {filepath}")
    print(f"Type: {entry.get('type', 'unknown')}")
    print(f"{'='*60}\n")

    entry_type = entry.get('type')

    if entry_type == 'word':
        print(f"Part of Speech: {entry.get('part_of_speech', 'N/A')}")
        print(f"\nMeaning: {entry.get('meaning', 'N/A')}")
        print(f"\nExamples:")
        for i, example in enumerate(entry.get('examples', []), 1):
            print(f"  {i}. {example}")

    elif entry_type == 'idiom':
        print(f"Meaning: {entry.get('meaning', 'N/A')}")
        print(f"\nExamples:")
        for i, example in enumerate(entry.get('examples', []), 1):
            print(f"  {i}. {example}")

    elif entry_type == 'terminology':
        print(f"Context: {entry.get('context', 'N/A')}")
        print(f"\nMeaning: {entry.get('meaning', 'N/A')}")
        print(f"\nExample: {entry.get('example', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(description='Show vocabulary entries due for review')
    parser.add_argument('--days', type=int, default=7,
                        help='Number of days before an entry is due for review (default: 7)')
    parser.add_argument('--limit', type=int, default=20,
                        help='Maximum number of entries to show (default: 20)')
    parser.add_argument('--all', action='store_true',
                        help='Show all due entries, ignoring the limit')

    args = parser.parse_args()

    # Get all entries
    entry_files = get_all_entries()

    if not entry_files:
        print("No vocabulary entries found.")
        print("Create entries using: ./add_entry.py")
        return 0

    # Filter for entries due for review
    due_entries = []
    for filepath in entry_files:
        try:
            entry = load_entry(filepath)
            if is_due_for_review(entry, args.days):
                due_entries.append((filepath, entry))
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")

    # Apply limit unless --all is specified
    if not args.all and len(due_entries) > args.limit:
        due_entries = due_entries[:args.limit]

    # Display results
    if not due_entries:
        print(f"No entries are due for review (checked with {args.days}-day interval).")
        print("\nTo see all entries and their status, run: ./status.py")
        return 0

    print(f"Found {len(due_entries)} entries due for review:\n")

    for index, (filepath, entry) in enumerate(due_entries, 1):
        display_entry(filepath, entry, index, len(due_entries))

    print(f"\n{'='*60}")
    print(f"\nAfter reviewing, mark these entries as reviewed with:")
    print(f"  ./mark_reviewed.py")
    print(f"\nOr mark specific entries:")
    print(f"  ./mark_reviewed.py <entry-name-1> <entry-name-2> ...")

    return 0


if __name__ == '__main__':
    exit(main())
