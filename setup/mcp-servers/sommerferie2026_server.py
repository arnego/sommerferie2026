"""
sommerferie2026_server.py  –  WSL-versjon
==========================================
MCP-server for familie Goderstad sin campingvognferie juli 2026.

Oppdaterer docs/ og index.html i GitHub-repo arnego/sommerferie2026 via
git commit + push. Siden publiseres automatisk på GitHub Pages:
https://arnego.github.io/sommerferie2026/

Arbeidsflyt for innholdsendringer:
  1. Oppdater relevant spec i docs/ (Ferieplanen-2026.md eller Teknisk-spesifikasjon.md)
  2. Oppdater index.html basert på den oppdaterte spec-en
  3. Commit + push begge filer i én operasjon

Plassering i WSL:
  /mnt/e/Git/sommerferie2026/setup/mcp-servers/sommerferie2026_server.py

Repo:
  /mnt/e/Git/sommerferie2026/

Krav:
  pip3 install mcp anthropic --break-system-packages
"""

import subprocess
import os
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

HTML_UPDATE_SYSTEM_PROMPT = EXPERT_ROLE + """
Du mottar en oppdateringsforespørsel, den relevante spec-filen og den nåværende index.html.
Returner KUN den oppdaterte, komplette index.html – ingenting annet.
Ingen forklaring, ingen markdown, bare ren HTML fra <!DOCTYPE html> til </html>.

Regler:
- Bevar all design, fargepalett og funksjonalitet (Tailwind, Alpine.js, Leaflet)
- Gjør kun de forespurte endringene
- Hold data i index.html konsistent med spec-filen
- Oppdater "Sist oppdatert" i footer med dagens dato hvis den finnes
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

def call_claude(system: str, user: str, max_tokens: int = 32000) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}]
    )
    return response.content[0].text

def update_spec_with_claude(instruction: str, current_spec: str) -> str:
    return call_claude(
        system=SPEC_UPDATE_SYSTEM_PROMPT,
        user=f"Oppdateringsforespørsel: {instruction}\n\n---\nNåværende spec:\n{current_spec}"
    )

def update_html_with_claude(instruction: str, updated_spec: str, current_html: str) -> str:
    return call_claude(
        system=HTML_UPDATE_SYSTEM_PROMPT,
        user=(
            f"Oppdateringsforespørsel: {instruction}\n\n"
            f"---\nOppdatert spec (Ferieplanen-2026.md):\n{updated_spec}\n\n"
            f"---\nNåværende index.html:\n{current_html}"
        )
    )


# ── VERKTØY ───────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="update_travel_plan",
            description=(
                "Oppdaterer reiseplanen for familie Goderstad sin campingvognferie juli 2026. "
                "Oppdaterer først Ferieplanen-2026.md (spec), deretter index.html basert på "
                "den oppdaterte spec-en, og committer + pusher begge filer til "
                "https://github.com/arnego/sommerferie2026. "
                "GitHub Pages publiserer siden automatisk på "
                "https://arnego.github.io/sommerferie2026/ etter ~30 sekunder. "
                "Brukes når noen vil endre rute, stopp, campingplasser, aktiviteter, "
                "budsjett, huskeliste, datoer eller annet innhold i reiseplanen."
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
            # Steg 1: Oppdater Ferieplanen-2026.md
            current_spec = read_file(FERIEPLAN_FILE)
            updated_spec = update_spec_with_claude(instruction, current_spec)
            write_file(FERIEPLAN_FILE, updated_spec)

            # Steg 2: Oppdater index.html basert på oppdatert spec
            current_html = read_file(INDEX_FILE)
            updated_html = update_html_with_claude(instruction, updated_spec, current_html)

            stripped_html = updated_html.strip()
            if not stripped_html.startswith("<!") or not stripped_html.endswith("</html>"):
                # Rull tilbake spec-endringen
                write_file(FERIEPLAN_FILE, current_spec)
                tail = stripped_html[-120:] if len(stripped_html) > 120 else stripped_html
                return [types.TextContent(
                    type="text",
                    text=(
                        f"Feil: Fikk ikke komplett HTML tilbake (trolig avkuttet av max_tokens).\n"
                        f"Generert: {len(stripped_html)} tegn. Siste 120 tegn: ...{tail}\n"
                        f"Spec-endringen er rullet tilbake."
                    )
                )]

            write_file(INDEX_FILE, updated_html)

            # Steg 3: Commit + push begge filer
            success, git_output = git_push(
                commit_message,
                files=["docs/Ferieplanen-2026.md", "index.html"]
            )

            if success:
                return [types.TextContent(
                    type="text",
                    text=(
                        f"Reiseplanen er oppdatert og pushet til GitHub!\n"
                        f"Commit: \"{commit_message[:72]}\"\n"
                        f"Endret: Ferieplanen-2026.md + index.html\n"
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
