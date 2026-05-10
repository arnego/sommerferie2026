"""
sommerferie2026_server.py  –  WSL-versjon
==========================================
MCP-server for familie Goderstad sin campingvognferie juli 2026.

Oppdaterer docs/ og index.html i GitHub-repo arnego/sommerferie2026 via
git commit + push. Siden publiseres automatisk på GitHub Pages:
https://arnego.github.io/sommerferie2026/

Arbeidsflyt for innholdsendringer (update_travel_plan):
  1. Claude foreslår en JSON-liste med {old_string, new_string}-erstatninger
     for både Ferieplanen-2026.md og index.html
  2. Serveren påfører erstatningene deterministisk (krever unik old_string)
  3. Commit + push begge filer i én operasjon

Arbeidsflyt for teknisk spec (update_technical_spec):
  1. Regenererer Teknisk-spesifikasjon.md i sin helhet via Claude
  2. Commit + push

Plassering i WSL:
  /mnt/e/Git/sommerferie2026/setup/mcp-servers/sommerferie2026_server.py

Repo:
  /mnt/e/Git/sommerferie2026/

Krav:
  pip3 install mcp anthropic --break-system-packages
"""

import subprocess
import os
import json
import time
from pathlib import Path
from datetime import datetime
import anthropic
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ── KONFIGURASJON ─────────────────────────────────────────────────
REPO_PATH        = Path("/mnt/e/Git/sommerferie2026")
INDEX_FILE       = REPO_PATH / "index.html"
FERIEPLAN_FILE   = REPO_PATH / "docs" / "Ferieplanen-2026.md"
TEKNISK_SPEC_FILE = REPO_PATH / "docs" / "Teknisk-spesifikasjon.md"
PAGES_URL        = "https://arnego.github.io/sommerferie2026/"
GITHUB_REPO      = "https://github.com/arnego/sommerferie2026"
MODEL            = "claude-sonnet-4-6"
# ──────────────────────────────────────────────────────────────────

server = Server("sommerferie2026")

EXPERT_ROLE = """Du er ekspert webutvikler og reisekonsulent for familie Goderstad sin campingvognferie juli 2026.
Du vet alt som bør være med for å planlegge en vellykket ferie, og for å lage en god presentasjon
av turen og reiserutene i nettformat.

Familien: Ann Kristin (42), Arne (40) og William (5 år).
Kjøretøy: Campingvogn Knaus Sport 400 LK, trukket av Land Rover Discovery 4.
Rute: Kongsberg → Løkken → Silkeborg → Lübeck → Billund → Berlin → Bad Schandau → Møns Klint → København → Go Nordic Cruiseline til Oslo → Kongsberg.
Publisert på: https://arnego.github.io/sommerferie2026/
"""

SPEC_UPDATE_SYSTEM_PROMPT = EXPERT_ROLE + """
Du mottar en oppdateringsforespørsel og den nåværende spec-filen (Markdown).
Returner KUN den oppdaterte, komplette Markdown-filen – ingenting annet.
Ingen forklaring, ingen kodeblokk-wrapper, bare ren Markdown.

Regler:
- Bevar all eksisterende struktur og formattering
- Gjør kun de forespurte endringene
- Oppdater endringsloggen nederst i dokumentet med dagens dato og en kort beskrivelse
"""

EDIT_SYSTEM_PROMPT = EXPERT_ROLE + """
Du mottar en oppdateringsforespørsel sammen med Ferieplanen-2026.md (spec) og index.html.
Din oppgave er å foreslå presise tekst-erstatninger som realiserer endringen.

Returner KUN ren JSON (ingen markdown-kodeblokker, ingen forklaring, ingen tekst rundt)
med følgende struktur:

{
  "spec_edits": [
    {"old_string": "<eksakt tekst i spec>", "new_string": "<ny tekst>", "description": "<kort>", "replace_all": false}
  ],
  "html_edits": [
    {"old_string": "<eksakt tekst i HTML>", "new_string": "<ny tekst>", "description": "<kort>", "replace_all": false}
  ]
}

KRITISKE REGLER for old_string:
- Må være EKSAKT tekst fra filen, inkludert mellomrom, linjeskift, tegnsetting og HTML-tagger.
- Som standard (replace_all=false) må old_string forekomme NØYAKTIG ÉN gang i filen.
  Hvis konteksten er tvetydig, inkluder nok omkringliggende tekst til at strengen blir unik.
- Sett replace_all=true KUN hvis du faktisk vil erstatte alle forekomster (f.eks. globalt navnebytte).
- Hold strengene så korte som mulig samtidig som de er unike.
- Aldri regex – ren tekst-matching.

KRITISKE REGLER for innhold:
- Gjør kun de forespurte endringene. Behold all annen struktur, design, fargepalett og
  funksjonalitet (Tailwind, Alpine.js, Leaflet).
- Hold data i index.html konsistent med spec-filen.
- Legg til ett spec_edits-element som oppdaterer endringsloggen nederst i
  Ferieplanen-2026.md med dagens dato og en kort beskrivelse av endringen.
- Oppdater "Sist oppdatert"-feltet i HTML-footeren hvis det finnes.
- Hvis en fil ikke trenger endringer, returner tom liste [].
- Foretrekk få brede edits framfor mange små når endringer henger sammen i samme blokk.
"""


# ── FILHJELP ──────────────────────────────────────────────────────

def read_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Finner ikke {path}")
    return path.read_text(encoding="utf-8")

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ── GIT ───────────────────────────────────────────────────────────

def git_push(commit_message: str, files: list[str]) -> tuple[bool, str]:
    """Committer og pusher gitte filer til GitHub via git i WSL."""
    try:
        output = []

        # git add for hver fil
        for f in files:
            result = subprocess.run(
                ["git", "-C", str(REPO_PATH), "add", f],
                capture_output=True, text=True,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
            )
            output.append(result.stdout + result.stderr)
            if result.returncode != 0:
                return False, "\n".join(output)

        # git commit
        result = subprocess.run(
            ["git", "-C", str(REPO_PATH), "commit", "-m",
             f"Signal: {commit_message[:72]}"],
            capture_output=True, text=True,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        )
        combined = result.stdout + result.stderr
        output.append(combined)
        if result.returncode != 0 and "nothing to commit" not in combined:
            return False, "\n".join(output)

        # git pull --rebase + push
        for cmd in [
            ["git", "-C", str(REPO_PATH), "pull", "--rebase"],
            ["git", "-C", str(REPO_PATH), "push"],
        ]:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
            )
            output.append(result.stdout + result.stderr)
            if result.returncode != 0:
                return False, "\n".join(output)

        return True, "\n".join(output)
    except Exception as e:
        return False, str(e)


# ── CLAUDE-KALL ───────────────────────────────────────────────────

def call_claude(system: str, user: str, max_tokens: int = 64000) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    chunks: list[str] = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for text in stream.text_stream:
            chunks.append(text)
    return "".join(chunks)

def update_spec_with_claude(instruction: str, current_spec: str) -> str:
    return call_claude(
        system=SPEC_UPDATE_SYSTEM_PROMPT,
        user=f"Oppdateringsforespørsel: {instruction}\n\n---\nNåværende spec:\n{current_spec}"
    )

def generate_edits(instruction: str, current_spec: str, current_html: str) -> dict:
    """Ber Claude foreslå targeted edits for spec + HTML, returnerer parsed JSON.

    Bruker prompt caching på systemprompten og filinnholdet: cache-lesninger
    teller bare 10 % mot rate-limit-kvoten, noe som løser 30k tokens/min-grensen.
    Prøver opptil 3 ganger med 30s ventetid ved RateLimitError (kald cache-miss).
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    for attempt in range(3):
        try:
            chunks: list[str] = []
            with client.messages.stream(
                model=MODEL,
                max_tokens=16000,
                system=[{
                    "type": "text",
                    "text": EDIT_SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"Nåværende Ferieplanen-2026.md:\n{current_spec}\n\n"
                                f"---\nNåværende index.html:\n{current_html}"
                            ),
                            "cache_control": {"type": "ephemeral"},
                        },
                        {
                            "type": "text",
                            "text": f"Oppdateringsforespørsel: {instruction}",
                        },
                    ],
                }],
            ) as stream:
                for text in stream.text_stream:
                    chunks.append(text)
            break
        except anthropic.RateLimitError:
            if attempt == 2:
                raise
            time.sleep(30 * (attempt + 1))

    raw = "".join(chunks).strip()
    if raw.startswith("```"):
        first_nl = raw.find("\n")
        if first_nl != -1:
            raw = raw[first_nl + 1:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
    return json.loads(raw)


def apply_edits(content: str, edits: list[dict]) -> tuple[str, list[str]]:
    """Påfør edits sekvensielt med unik-match-validering.

    Returnerer (oppdatert_innhold, liste_med_feil). Edit feiler hvis old_string
    ikke finnes, eller hvis den finnes flere ganger uten replace_all=true.
    """
    errors = []
    for i, edit in enumerate(edits):
        old = edit.get("old_string", "")
        new = edit.get("new_string", "")
        desc = edit.get("description") or f"edit {i + 1}"
        replace_all = bool(edit.get("replace_all", False))

        if not old:
            errors.append(f"'{desc}': mangler old_string")
            continue
        count = content.count(old)
        if count == 0:
            errors.append(f"'{desc}': old_string ikke funnet i filen")
            continue
        if count > 1 and not replace_all:
            errors.append(
                f"'{desc}': old_string forekommer {count} ganger – sett replace_all=true "
                f"hvis dette er ønsket, ellers utvid old_string så den blir unik"
            )
            continue
        if replace_all:
            content = content.replace(old, new)
        else:
            content = content.replace(old, new, 1)
    return content, errors


# ── VERKTØY ───────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="update_travel_plan",
            description=(
                "Oppdaterer reiseplanen for familie Goderstad sin campingvognferie juli 2026. "
                "Bruker presise tekst-erstatninger (targeted edits) i både "
                "Ferieplanen-2026.md (spec) og index.html, og committer + pusher begge "
                "filer til https://github.com/arnego/sommerferie2026. GitHub Pages "
                "publiserer siden automatisk på https://arnego.github.io/sommerferie2026/ "
                "etter ~30 sekunder. Brukes når noen vil endre rute, stopp, campingplasser, "
                "aktiviteter, budsjett, huskeliste, datoer eller annet innhold i reiseplanen. "
                "Egnet både for små punktendringer og større omskrivinger så lenge endringen "
                "kan uttrykkes som tekst-erstatninger (ikke krever full restrukturering)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "instruction": {
                        "type": "string",
                        "description": "Hva som skal endres i reiseplanen. Vær spesifikk."
                    },
                    "commit_message": {
                        "type": "string",
                        "description": (
                            "Valgfri git commit-melding. Hvis ikke oppgitt brukes "
                            "en automatisk generert melding basert på instruksjonen."
                        )
                    }
                },
                "required": ["instruction"]
            }
        ),
        types.Tool(
            name="update_technical_spec",
            description=(
                "Oppdaterer kun den tekniske spesifikasjonen (Teknisk-spesifikasjon.md) "
                "uten å endre index.html. Brukes for endringer i designkrav, tekniske krav, "
                "funksjonelle krav, verifiseringsprosedyre eller fremtidige muligheter."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "instruction": {
                        "type": "string",
                        "description": "Hva som skal endres i den tekniske spesifikasjonen."
                    },
                    "commit_message": {
                        "type": "string",
                        "description": "Valgfri git commit-melding."
                    }
                },
                "required": ["instruction"]
            }
        ),
        types.Tool(
            name="read_travel_plan",
            description=(
                "Leser og returnerer metadata om den nåværende reiseplanen: "
                "index.html og Ferieplanen-2026.md fra ~/projects/sommerferie2026/."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        types.Tool(
            name="get_travel_plan_url",
            description=(
                "Returnerer URL til den publiserte reiseplanen på GitHub Pages "
                "og lenke til GitHub-repoet."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []}
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    if name == "get_travel_plan_url":
        return [types.TextContent(
            type="text",
            text=f"GitHub Pages: {PAGES_URL}\nGitHub repo: {GITHUB_REPO}"
        )]

    if name == "read_travel_plan":
        try:
            html = read_file(INDEX_FILE)
            spec = read_file(FERIEPLAN_FILE)
            html_mtime = datetime.fromtimestamp(INDEX_FILE.stat().st_mtime).strftime("%d.%m.%Y %H:%M")
            spec_mtime = datetime.fromtimestamp(FERIEPLAN_FILE.stat().st_mtime).strftime("%d.%m.%Y %H:%M")
            return [types.TextContent(
                type="text",
                text=(
                    f"index.html: {len(html)} tegn, sist endret {html_mtime}\n"
                    f"Ferieplanen-2026.md: {len(spec)} tegn, sist endret {spec_mtime}\n"
                    f"GitHub Pages: {PAGES_URL}\n"
                    f"GitHub repo: {GITHUB_REPO}"
                )
            )]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Feil: {e}")]

    if name == "update_travel_plan":
        instruction = arguments.get("instruction", "").strip()
        if not instruction:
            return [types.TextContent(type="text", text="Mangler instruksjon.")]

        commit_message = arguments.get("commit_message", "").strip() or instruction

        try:
            current_spec = read_file(FERIEPLAN_FILE)
            current_html = read_file(INDEX_FILE)

            # Steg 1: Be Claude foreslå targeted edits som JSON
            try:
                edits = generate_edits(instruction, current_spec, current_html)
            except json.JSONDecodeError as e:
                return [types.TextContent(
                    type="text",
                    text=f"Feil: Klarte ikke parse edits-JSON fra Claude: {e}"
                )]

            spec_edits = edits.get("spec_edits") or []
            html_edits = edits.get("html_edits") or []

            if not spec_edits and not html_edits:
                return [types.TextContent(
                    type="text",
                    text="Ingen endringer foreslått. Prøv å omformulere instruksjonen mer spesifikt."
                )]

            # Steg 2: Påfør edits in-memory og samle alle feil før vi skriver noe
            new_spec, spec_errors = apply_edits(current_spec, spec_edits)
            new_html, html_errors = apply_edits(current_html, html_edits)

            if spec_errors or html_errors:
                problem = []
                if spec_errors:
                    problem.append("Spec-feil:\n  - " + "\n  - ".join(spec_errors))
                if html_errors:
                    problem.append("HTML-feil:\n  - " + "\n  - ".join(html_errors))
                return [types.TextContent(
                    type="text",
                    text=(
                        "Edits feilet – ingen filer endret.\n\n"
                        + "\n\n".join(problem)
                        + "\n\nPrøv å være mer spesifikk om hvor i dokumentet endringen skal skje."
                    )
                )]

            # Steg 3: Skriv kun filene som faktisk endret seg
            files_changed = []
            if new_spec != current_spec:
                write_file(FERIEPLAN_FILE, new_spec)
                files_changed.append("docs/Ferieplanen-2026.md")
            if new_html != current_html:
                write_file(INDEX_FILE, new_html)
                files_changed.append("index.html")

            if not files_changed:
                return [types.TextContent(
                    type="text",
                    text="Edits ble påført, men gav ingen netto endring. Ingenting committet."
                )]

            # Steg 4: Commit + push
            success, git_output = git_push(commit_message, files=files_changed)

            edit_summary = []
            for e in spec_edits:
                edit_summary.append(f"  - spec: {e.get('description') or '(uten beskrivelse)'}")
            for e in html_edits:
                edit_summary.append(f"  - html: {e.get('description') or '(uten beskrivelse)'}")

            if success:
                return [types.TextContent(
                    type="text",
                    text=(
                        f"Reiseplanen er oppdatert og pushet til GitHub!\n"
                        f"Commit: \"{commit_message[:72]}\"\n"
                        f"Filer endret: {', '.join(files_changed)}\n"
                        f"Endringer:\n" + "\n".join(edit_summary) + "\n"
                        f"GitHub Pages oppdateres om ~30 sekunder.\n"
                        f"{PAGES_URL}"
                    )
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=(
                        f"Filene er oppdatert lokalt, men git push feilet:\n"
                        f"{git_output[:400]}"
                    )
                )]

        except Exception as e:
            return [types.TextContent(type="text", text=f"Feil: {e}")]

    if name == "update_technical_spec":
        instruction = arguments.get("instruction", "").strip()
        if not instruction:
            return [types.TextContent(type="text", text="Mangler instruksjon.")]

        commit_message = arguments.get("commit_message", "").strip() or instruction

        try:
            current_spec = read_file(TEKNISK_SPEC_FILE)
            updated_spec = update_spec_with_claude(instruction, current_spec)
            write_file(TEKNISK_SPEC_FILE, updated_spec)

            success, git_output = git_push(
                commit_message,
                files=["docs/Teknisk-spesifikasjon.md"]
            )

            if success:
                return [types.TextContent(
                    type="text",
                    text=(
                        f"Teknisk-spesifikasjon.md er oppdatert og pushet!\n"
                        f"Commit: \"{commit_message[:72]}\""
                    )
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"Spec oppdatert lokalt, men git push feilet:\n{git_output[:400]}"
                )]

        except Exception as e:
            return [types.TextContent(type="text", text=f"Feil: {e}")]

    return [types.TextContent(type="text", text=f"Ukjent verktøy: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
