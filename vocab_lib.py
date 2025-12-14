"""
Shared library for vocabulary entry validation and utilities.
"""

from pathlib import Path
from datetime import datetime, timedelta
import yaml


def load_entry(filepath):
    """Load a YAML entry file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def save_entry(filepath, entry_data):
    """Save entry data to a YAML file."""
    with open(filepath, 'w') as f:
        yaml.dump(entry_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def is_promoted_word(entry):
    """Check if a word entry has all required fields."""
    required_fields = ['name', 'part_of_speech', 'meaning', 'examples']

    for field in required_fields:
        if field not in entry or entry[field] is None:
            return False
        # Examples must be a non-empty list
        if field == 'examples' and (not isinstance(entry[field], list) or len(entry[field]) == 0):
            return False

    return True


def is_promoted_idiom(entry):
    """Check if an idiom entry has all required fields."""
    required_fields = ['name', 'meaning', 'examples']

    for field in required_fields:
        if field not in entry or entry[field] is None:
            return False
        # Examples must be a non-empty list
        if field == 'examples' and (not isinstance(entry[field], list) or len(entry[field]) == 0):
            return False

    return True


def is_promoted_terminology(entry):
    """Check if a terminology entry has all required fields."""
    required_fields = ['name', 'context', 'meaning', 'example']

    for field in required_fields:
        if field not in entry or entry[field] is None:
            return False

    return True


def is_promoted(entry):
    """Check if an entry is promoted (has all required fields)."""
    entry_type = entry.get('type')

    if entry_type == 'word':
        return is_promoted_word(entry)
    elif entry_type == 'idiom':
        return is_promoted_idiom(entry)
    elif entry_type == 'terminology':
        return is_promoted_terminology(entry)

    return False


def is_due_for_review(entry, days=7):
    """Check if an entry is due for review."""
    # Only promoted entries are eligible for review
    if not is_promoted(entry):
        return False

    last_reviewed = entry.get('last_reviewed')

    # If never reviewed, it's due
    if last_reviewed is None:
        return True

    # Parse the last reviewed date
    if isinstance(last_reviewed, str):
        last_reviewed_date = datetime.fromisoformat(last_reviewed)
    else:
        last_reviewed_date = last_reviewed

    # Check if enough days have passed
    days_since_review = (datetime.now() - last_reviewed_date).days
    return days_since_review >= days


def get_all_entries():
    """Get all entry files from all directories."""
    entries = []

    for directory in ['words', 'idioms', 'terminologies']:
        dir_path = Path(directory)
        if dir_path.exists():
            for filepath in dir_path.glob('*.yaml'):
                entries.append(filepath)

    return entries


def get_entry_status(entry):
    """Get a human-readable status for an entry."""
    if is_promoted(entry):
        if entry.get('last_reviewed') is None:
            return 'promoted (never reviewed)'
        else:
            return 'promoted (reviewed)'
    else:
        return 'stub'
