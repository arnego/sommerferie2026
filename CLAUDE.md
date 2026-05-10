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

## Publisering av endringer

Etter hver endring i `index.html` eller dokumentene i `docs/` skal Claude:
1. Oppdatere endringsloggen i det relevante dokumentet (`Ferieplanen-2026.md` eller `Teknisk-spesifikasjon.md`)
2. Gjøre `git add` på endrede filer
3. Gjøre `git commit` med en beskrivende melding om hva som ble endret
4. Gjøre `git push` for å publisere til GitHub Pages

Claude har tillatelse til å gjøre `git pull --rebase`, `git commit` og `git push` uten å spørre først.

Websiden er tilgjengelig på: `https://arnego.github.io/sommerferie2026/`

## URL-kvalitetskontroll

**Regel: Alle URL-er skal verifiseres med WebFetch før de legges inn i kode eller dokumenter.**

Dette gjelder URL-er til campingplasser, aktiviteter, ferger, bookingplattformer og alle andre eksterne lenker.

### Fremgangsmåte

1. **Bruk WebFetch** på URL-en før den skrives inn i `index.html` eller `docs/`.
2. **Sjekk at siden laster** (HTTP 200) og at innholdet matcher forventet sted/aktivitet (campingplassens navn, beliggenhet e.l. bør fremgå av siden).
3. **Finn korrekt URL via WebSearch** dersom WebFetch feiler, gir 404, eller innholdet ikke stemmer.
4. **Ikke legg inn URL-er fra hukommelse/treningsdata alene** — disse er ofte utdaterte, feilstavet eller peker på feil side.

### Hvis verifisering ikke er mulig

Dersom WebFetch ikke er tilgjengelig i konteksten: legg inn URL-en med en kommentar `// TODO: verifiser URL` og oppgi at URL-en er uverifisert i svar til bruker.

## GitHub Automation

Two GitHub Actions workflows are configured:
- **`claude.yml`**: Claude PR assistant — triggers on `@claude` mentions in issues, PR comments, and reviews.
- **`claude-code-review.yml`**: Automatic Claude code review on every PR open/update using the `code-review` plugin.

Both require `CLAUDE_CODE_OAUTH_TOKEN` set as a repository secret.
