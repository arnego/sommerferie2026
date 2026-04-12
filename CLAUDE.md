# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

In this project Claude Code serves as an expert web developer and travel consultant. Claude knows everything that should be included in order to plan a successful vacation, and to create a good presentation of the trip and itineraries in web format. The product is a single-file HTML page for the summer holiday 2026 trip plan. 

## Development

The project is governed by two specification documents in `docs/`:
- `docs/Ferieplanen-2026.md` — reiseplan med alle stopp, aktiviteter og praktisk info
- `docs/Teknisk-spesifikasjon.md` — tekniske krav, design, funksjonalitet og verifisering

For local testing, use the HTTPS server:
```
python setup/test-server/https_server.py
```
Open `https://localhost:3000/index.html` in Chrome.

## Architecture



## GitHub Automation

Two GitHub Actions workflows are configured:
- **`claude.yml`**: Claude PR assistant — triggers on `@claude` mentions in issues, PR comments, and reviews.
- **`claude-code-review.yml`**: Automatic Claude code review on every PR open/update using the `code-review` plugin.

Both require `CLAUDE_CODE_OAUTH_TOKEN` set as a repository secret.
