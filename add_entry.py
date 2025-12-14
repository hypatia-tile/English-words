#!/usr/bin/env python3
"""
Add a new vocabulary entry (word, idiom, or terminology).
Creates a stub entry that can be refined later.
"""

import argparse
import uuid
import yaml
from pathlib import Path
from datetime import datetime


def create_word_stub(name, example):
    """Create a minimal word stub."""
    return {
        'id': str(uuid.uuid4()),
        'name': name,
        'type': 'word',
        'created_at': datetime.now().isoformat(),
        'part_of_speech': None,
        'meaning': None,
        'examples': [example] if example else [],
        'last_reviewed': None
    }


def create_idiom_stub(name, example):
    """Create a minimal idiom stub."""
    return {
        'id': str(uuid.uuid4()),
        'name': name,
        'type': 'idiom',
        'created_at': datetime.now().isoformat(),
        'meaning': None,
        'examples': [example] if example else [],
        'last_reviewed': None
    }


def create_terminology_stub(name, context, example):
    """Create a minimal terminology stub."""
    return {
        'id': str(uuid.uuid4()),
        'name': name,
        'type': 'terminology',
        'created_at': datetime.now().isoformat(),
        'context': context,
        'meaning': None,
        'example': example,
        'last_reviewed': None
    }


def slugify(text):
    """Convert text to a safe filename."""
    return text.lower().replace(' ', '-').replace('/', '-')


def save_entry(entry_type, entry_data):
    """Save the entry to the appropriate directory."""
    # Determine the directory
    dir_map = {
        'word': 'words',
        'idiom': 'idioms',
        'terminology': 'terminologies'
    }
    directory = Path(dir_map[entry_type])
    directory.mkdir(exist_ok=True)

    # Create filename from name (slug)
    slug = slugify(entry_data['name'])
    filename = directory / f"{slug}.yaml"

    # Check if file already exists
    if filename.exists():
        print(f"Warning: Entry '{entry_data['name']}' already exists at {filename}")
        return None

    # Write YAML file
    with open(filename, 'w') as f:
        yaml.dump(entry_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return filename


def main():
    parser = argparse.ArgumentParser(description='Add a new vocabulary entry')
    parser.add_argument('type', choices=['word', 'idiom', 'terminology'],
                        help='Type of entry to create')
    parser.add_argument('name', help='The word, idiom, or terminology')
    parser.add_argument('--example', help='Example sentence')
    parser.add_argument('--context', help='Context (required for terminology)')

    args = parser.parse_args()

    # Create the appropriate stub
    if args.type == 'word':
        entry = create_word_stub(args.name, args.example)
    elif args.type == 'idiom':
        entry = create_idiom_stub(args.name, args.example)
    elif args.type == 'terminology':
        if not args.context:
            print("Error: --context is required for terminology entries")
            return 1
        entry = create_terminology_stub(args.name, args.context, args.example)

    # Save the entry
    filename = save_entry(args.type, entry)

    if filename:
        print(f"Created stub entry: {filename}")
        print(f"ID: {entry['id']}")
        print("\nYou can now edit this file to add more details.")
        print("The entry will become reviewable once all required fields are filled.")
    else:
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
