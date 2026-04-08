# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a single-file static HTML demo page for a summer holiday 2026 trip plan — a caravan journey from Kongsberg, Norway through Europe to the Alps and back (4 weeks, July 2026). The entire app lives in `index.html` with no build system, no dependencies, and no backend.

## Development

Open `index.html` directly in a browser. No build, install, or serve step is required.

## Architecture

Everything is in one file (`index.html`):
- **CSS**: Inline `<style>` block with CSS custom properties (`--sand`, `--terracotta`, `--olive`, `--navy`, `--gold`, `--muted`) for the color palette.
- **HTML**: Sections in order — hero banner, stats bar, route visual, collapsible week cards, checklist, budget grid, notes textarea.
- **JS**: Minimal inline `<script>` — `toggleWeek()` for accordion cards, checkbox state toggling. No persistence beyond the page session.

## GitHub Automation

Two GitHub Actions workflows are configured:
- **`claude.yml`**: Claude PR assistant — triggers on `@claude` mentions in issues, PR comments, and reviews.
- **`claude-code-review.yml`**: Automatic Claude code review on every PR open/update using the `code-review` plugin.

Both require `CLAUDE_CODE_OAUTH_TOKEN` set as a repository secret.
