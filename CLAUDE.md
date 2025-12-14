# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **local-first vocabulary learning system** for capturing and reviewing English words, idioms, and terminologies encountered during technical reading. The system uses daily script-driven review with spaced repetition.

## Architecture

### Directory Structure

The content is organized into three top-level directories:
- `words/` - Individual English words
- `idioms/` - Idiomatic expressions
- `terminologies/` - Technical terms and jargon

Each item is stored as **one file per entry** containing an explicit ID.

### Entry Lifecycle Model

Entries progress through two implicit states:

1. **Stub** - Minimal capture form (surface form + one example sentence)
   - Not eligible for review
   - Quick capture during reading (~1 minute)

2. **Promoted Entry** - Becomes reviewable when all required fields are present
   - No explicit status flag needed
   - Promotion happens implicitly when validation passes

### Required Fields by Type

**Word:**
- name
- part of speech
- meaning
- examples

**Idiom:**
- name
- meaning
- examples

**Terminology:**
- name
- context
- meaning
- example

### Review System Design

- **Trigger:** Daily execution
- **Selection logic:** Items where `last-reviewed date >= N days`
  - N is configurable per type (word/idiom/terminology)
  - Target: 10-20 items per day
- **Review metadata:** Stored inside each item file (last-reviewed date only)

## Development Principles

### Key Constraints

- **Everything runs locally** - no server components
- **Low friction capture** - stubs can be created quickly and refined later
- **Implicit promotion** - entries become reviewable when complete, no manual status changes

### Intentionally Deferred Decisions

These design choices are deliberately postponed and should be discussed before implementation:

- ID format/generation strategy
- File format (Markdown, YAML, JSON, etc.)
- Script language and CLI interface
- Field validation mechanism
- How to detect when required fields are present

### Workflow Pattern

The intended user workflow is:
1. Run script to see items "due today"
2. Review the items presented
3. Run script to update last-reviewed timestamps
4. Commit changes to GitHub

When implementing scripts, follow this workflow model and keep each step simple and transparent.
