# English Vocabulary Learning System

A local-first vocabulary learning system for capturing and reviewing English words, idioms, and terminologies with spaced repetition.

## Quick Start

```bash
# Setup (first time only)
./setup.sh

# Activate the environment
source venv/bin/activate

# Add a new word (stub)
python add_entry.py word "ephemeral" --example "The ephemeral nature of cloud infrastructure."

# See all entries and their status
python status.py

# Review entries due today
python review.py

# Mark reviewed entries
python mark_reviewed.py
```

## Features

- **Low-friction capture**: Create stub entries in seconds during reading
- **Implicit promotion**: Entries become reviewable when complete
- **Spaced repetition**: Configurable review intervals (default: 7 days)
- **Local-first**: Everything runs locally, commit to git when ready
- **Three content types**: Words, idioms, and terminologies

---

## Finalized Requirements (This Round)

### Core Purpose

* Capture English words, idioms, and terminologies encountered during technical reading
* Retain them through **daily, script-driven review**
* Keep friction low during reading, allow refinement later

---

### Structure & Identity

* Separate directories:

  * `words/`
  * `idioms/`
  * `terminologies/`
* One file per item
* Each file contains an **explicit ID** (format undecided)

---

### Entry Lifecycle

#### 1. Stub

* Minimum required:

  * surface form
  * one example sentence
* Added manually (~1 minute)
* **Not reviewable**
* Exists mainly for capture

#### 2. Promoted Entry

* Becomes reviewable **implicitly** when:

  * all required fields for its type are present
* No explicit status flag needed

---

### Content Requirements (Promotion Criteria)

* **Word**

  * name
  * part of speech
  * meaning
  * examples

* **Idiom**

  * name
  * meaning
  * examples

* **Terminology**

  * name
  * context
  * meaning
  * example

---

### Review System

* Trigger: **daily**
* Selection rule:

  * last-reviewed date ≥ N
  * **N is fixed but configurable**
  * **N differs per type**
* Review state:

  * last-reviewed date only
  * stored **inside each item file**
* Daily volume target: ~10–20 items

---

### Workflow

* Everything runs **locally**
* You:

  1. Run a script to see “due today”
  2. Review items
  3. Run a script to update last-reviewed
  4. Commit to GitHub

---

### Implementation Decisions

* **ID format**: UUID
* **File format**: YAML
* **Script language**: Python 3
* **Validation**: Automatic detection of required fields
* **Review interval**: 7 days (configurable via `--days` flag)

## Scripts

### `add_entry.py`
Create new vocabulary entries (stubs).

```bash
# Add a word
python add_entry.py word "ephemeral" --example "Example sentence here."

# Add an idiom
python add_entry.py idiom "break the ice" --example "Example sentence here."

# Add a terminology
python add_entry.py terminology "eventual consistency" --context "distributed systems" --example "Example sentence here."
```

### `status.py`
View all entries and their current status.

```bash
# Show all entries
python status.py

# Filter by type
python status.py --type word

# Filter by status
python status.py --status stub
python status.py --status due
```

### `review.py`
Display entries due for review.

```bash
# Show entries due for review (default: 7 days)
python review.py

# Custom review interval
python review.py --days 3

# Show all due entries (no limit)
python review.py --all
```

### `mark_reviewed.py`
Update last-reviewed timestamp.

```bash
# Mark all due entries as reviewed
python mark_reviewed.py

# Mark specific entries
python mark_reviewed.py ephemeral "break the ice"
```

## File Structure

```
.
├── words/              # Word entries
├── idioms/             # Idiom entries
├── terminologies/      # Terminology entries
├── add_entry.py        # Create new entries
├── status.py           # View all entries
├── review.py           # Show entries due for review
├── mark_reviewed.py    # Update review timestamps
├── vocab_lib.py        # Shared validation logic
├── setup.sh            # Setup script
└── requirements.txt    # Python dependencies
```

## Daily Workflow

1. **Morning**: Run `python review.py` to see entries due for review
2. **Review**: Read through the presented entries
3. **Mark complete**: Run `python mark_reviewed.py` to update timestamps
4. **Commit**: `git add . && git commit -m "chore: review session" && git push`

During the day, capture new words as stubs and refine them when you have time.
