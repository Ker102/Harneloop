# Harneloop Rename Implementation Plan

> **For Agent:** Use executing-plans skill to implement this plan task-by-task.

**Goal:** Make Harneloop the only current product, package, CLI, configuration, documentation, repository, release, and local-workspace identity.

**Architecture:** Perform a private-alpha hard cutover without a deprecated CLI or import alias. Preserve immutable Git history, but add a repository test that rejects the legacy product token from current tracked paths and text files. Rename adjacent untracked planning and marketing material separately without committing the parent vault.

**Tech Stack:** Python 3.11+, setuptools, argparse, unittest, Git, GitHub CLI, Markdown, YAML, JSON.

---

### Task 1: Add The Rename Guard

**Files:**
- Modify: `tests/test_repo_structure.py`

1. Add a test that constructs the legacy token from two string fragments and scans tracked source, schema, test, and documentation paths and text content.
2. Assert that no current path or text contains the legacy token, case-insensitively.
3. Run the focused test and verify it fails against the existing tree.

### Task 2: Rename The Python Product Surface

**Files:**
- Rename: `src/<legacy-package>/` to `src/harneloop/`
- Modify: `pyproject.toml`
- Modify: `src/harneloop/**/*.py`
- Modify: `tests/**/*.py`

1. Rename the import package and console script to `harneloop`.
2. Rename the framework exception to `HarneloopError`.
3. Rename local home/config identity to `.harneloop` and `HARNELOOP_HOME`.
4. Rename generated package and adapter artifacts.
5. Run focused lifecycle, CLI, concurrency, and structure tests.

### Task 3: Rename Current Documentation And Assets

**Files:**
- Modify: `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`
- Modify: `docs/**/*.md`, `schemas/*.json`
- Rename: lifecycle image and any branded generated filenames

1. Replace current prose, commands, paths, URLs, schema IDs, package names, and headings.
2. Rewrite naming-status text so Harneloop is the chosen identity rather than a temporary name.
3. Keep historical case-study statements accurate while naming the current framework Harneloop.
4. Run the rename guard and link/path checks.

### Task 4: Reinstall And Verify The Local CLI

**Files:**
- Local virtual environment metadata only

1. Uninstall the legacy editable distribution from `.venv`.
2. Install Harneloop editable from the renamed package.
3. Verify `python -m harneloop`, `harneloop --help`, onboarding, diagnostics, and a temporary harness-unit lifecycle.
4. Verify the legacy console entrypoint is absent.

### Task 5: Rename Adjacent Vault Material

**Files:**
- Rename: `../<legacy>-marketing/` to `../harneloop-marketing/`
- Modify: adjacent marketing and architecture Markdown
- Modify: parent vault `.gitignore`
- Rename: current quick-note filenames containing the legacy product name

1. Replace current product references and paths in adjacent untracked vault material.
2. Rename the directories and quick notes.
3. Update the nested-repository ignore path.
4. Verify no current vault file or path contains the legacy token outside ignored Git history.

### Task 6: Commit And Move The Repository

**Files:**
- Git metadata and local directory path

1. Run the full suite, compile check, diagnostics, CLI smoke, and diff checks.
2. Commit the current-tree rename in the nested repository.
3. Rename the GitHub repository to `Ker102/Harneloop` and update `origin`.
4. Push the renamed current tree.
5. Rename the local nested repository directory to `harneloop`.

### Task 7: Recreate The Private-alpha Release

**Files:**
- GitHub release and tag metadata

1. Remove the old private-alpha release and tag.
2. Create `v0.0.1` at the final Harneloop rename commit.
3. Publish it as `Harneloop v0.0.1 - Private Alpha`.
4. Verify the release, tag target, remote repository, clean worktree, and absence of the legacy token from the current tree.
