# English-words
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

### Open / Intentionally Undecided

* ID format
* Exact file format (Markdown, YAML, etc.)
* Script language and interface
* How “required fields present” is validated

All of these can be decided later without breaking your model.
