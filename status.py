#!/usr/bin/env python3
"""
Show the status of all vocabulary entries.
"""

import argparse
from datetime import datetime
from vocab_lib import load_entry, get_all_entries, get_entry_status, is_promoted, is_due_for_review


def format_date(date_str):
    """Format a date string for display."""
    if date_str is None:
        return 'Never'

    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime('%Y-%m-%d')
    except:
        return str(date_str)


def main():
    parser = argparse.ArgumentParser(description='Show status of all vocabulary entries')
    parser.add_argument('--type', choices=['word', 'idiom', 'terminology'],
                        help='Filter by entry type')
    parser.add_argument('--status', choices=['stub', 'promoted', 'due'],
                        help='Filter by status (stub, promoted, or due for review)')
    parser.add_argument('--days', type=int, default=7,
                        help='Review interval in days (default: 7)')

    args = parser.parse_args()

    # Get all entries
    entry_files = get_all_entries()

    if not entry_files:
        print("No vocabulary entries found.")
        print("Create entries using: ./add_entry.py")
        return 0

    # Load and categorize entries
    stubs = []
    promoted_entries = []
    due_for_review = []

    for filepath in entry_files:
        try:
            entry = load_entry(filepath)

            # Apply type filter
            if args.type and entry.get('type') != args.type:
                continue

            entry_info = (filepath, entry)

            if is_due_for_review(entry, args.days):
                due_for_review.append(entry_info)
            elif is_promoted(entry):
                promoted_entries.append(entry_info)
            else:
                stubs.append(entry_info)

        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")

    # Apply status filter and display
    total = len(stubs) + len(promoted_entries) + len(due_for_review)

    print(f"Vocabulary Status Report")
    print(f"{'='*70}\n")
    print(f"Total entries: {total}")
    print(f"Review interval: {args.days} days\n")

    if args.status is None or args.status == 'stub':
        print(f"STUBS ({len(stubs)}) - Incomplete entries, not yet reviewable:")
        print("-" * 70)
        if stubs:
            for filepath, entry in stubs:
                missing = []
                if entry.get('type') == 'word':
                    if not entry.get('part_of_speech'): missing.append('part_of_speech')
                    if not entry.get('meaning'): missing.append('meaning')
                    if not entry.get('examples') or len(entry.get('examples', [])) == 0:
                        missing.append('examples')
                elif entry.get('type') == 'idiom':
                    if not entry.get('meaning'): missing.append('meaning')
                    if not entry.get('examples') or len(entry.get('examples', [])) == 0:
                        missing.append('examples')
                elif entry.get('type') == 'terminology':
                    if not entry.get('context'): missing.append('context')
                    if not entry.get('meaning'): missing.append('meaning')
                    if not entry.get('example'): missing.append('example')

                print(f"  • {entry['name']} ({entry.get('type', 'unknown')})")
                print(f"    File: {filepath}")
                print(f"    Missing: {', '.join(missing)}")
        else:
            print("  None")
        print()

    if args.status is None or args.status == 'due':
        print(f"DUE FOR REVIEW ({len(due_for_review)}) - Ready to review today:")
        print("-" * 70)
        if due_for_review:
            for filepath, entry in due_for_review:
                last_reviewed = format_date(entry.get('last_reviewed'))
                print(f"  • {entry['name']} ({entry.get('type', 'unknown')})")
                print(f"    Last reviewed: {last_reviewed}")
        else:
            print("  None")
        print()

    if args.status is None or args.status == 'promoted':
        print(f"PROMOTED ({len(promoted_entries)}) - Complete but not due for review:")
        print("-" * 70)
        if promoted_entries:
            for filepath, entry in promoted_entries:
                last_reviewed = format_date(entry.get('last_reviewed'))
                print(f"  • {entry['name']} ({entry.get('type', 'unknown')})")
                print(f"    Last reviewed: {last_reviewed}")
        else:
            print("  None")
        print()

    # Summary
    print("=" * 70)
    print("\nNext steps:")
    if stubs:
        print(f"  • Edit {len(stubs)} stub(s) to add missing fields")
    if due_for_review:
        print(f"  • Review {len(due_for_review)} entry/entries: ./review.py")
        print(f"  • After reviewing, mark as reviewed: ./mark_reviewed.py")
    if not stubs and not due_for_review:
        print(f"  • All entries are up to date!")

    return 0


if __name__ == '__main__':
    exit(main())
