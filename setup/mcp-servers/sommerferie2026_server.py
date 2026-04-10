"""
sommerferie2026_server.py  –  WSL-versjon
==========================================
MCP-server for familie Goderstad sin campingvognferie juli 2026.

Oppdaterer index.html i GitHub-repo arnego/sommerferie2026 via
git commit + push. Siden publiseres automatisk på GitHub Pages:
https://arnego.github.io/sommerferie2026/

Plassering i WSL:
  ~/projects/mcp-servers/sommerferie2026/sommerferie2026_server.py

Repo:
  ~/projects/sommerferie2026/

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
REPO_PATH  = Path("/home/arne/projects/sommerferie2026")
INDEX_FILE = REPO_PATH / "index.html"
PAGES_URL  = "https://arnego.github.io/sommerferie2026/"
GITHUB_REPO = "https://github.com/arnego/sommerferie2026"
MODEL      = "claude-sonnet-4-6"
# ──────────────────────────────────────────────────────────────────

server = Server("sommerferie2026")

UPDATE_SYSTEM_PROMPT = """Du vedlikeholder en HTML-reiseplan for en campingvognferie i juli 2026.
Ruten: Kongsberg → Göteborg → København → Hamburg → Amsterdam → Schwarzwald → Østerrike/Alpene

Du mottar en oppdateringsforespørsel og den nåværende index.html.
Returner KUN den oppdaterte, komplette index.html – ingenting annet.
Ingen forklaring, ingen markdown, bare ren HTML fra <!DOCTYPE html> til </html>.

Regler:
- Bevar all design og funksjonalitet
- Gjør kun de forespurte endringene
- Oppdater "Sist oppdatert" i footer med dagens dato
"""


def read_html() -> str:
    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Finner ikke {INDEX_FILE}\n"
            f"Sjekk at repoet ligger på ~/projects/sommerferie2026/"
        )
    return INDEX_FILE.read_text(encoding="utf-8")


def write_html(content: str):
    INDEX_FILE.write_text(content, encoding="utf-8")


def git_push(commit_message: str) -> tuple[bool, str]:
    """Committer og pusher til GitHub via git i WSL."""
    try:
        cmds = [
            ["git", "-C", str(REPO_PATH), "add", "index.html"],
            ["git", "-C", str(REPO_PATH), "commit", "-m",
             f"Signal: {commit_message[:72]}"],
            ["git", "-C", str(REPO_PATH), "push"],
        ]
        output = []
        for cmd in cmds:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
            )
            combined = result.stdout + result.stderr
            output.append(combined)
            if result.returncode != 0 and "nothing to commit" not in combined:
                return False, "\n".join(output)
        return True, "\n".join(output)
    except Exception as e:
        return False, str(e)


def call_claude_for_update(instruction: str, current_html: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=UPDATE_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"Oppdateringsforespørsel: {instruction}\n\n"
                f"---\nNåværende index.html:\n{current_html}"
            )
        }]
    )
    return response.content[0].text


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="update_travel_plan",
            description=(
                "Oppdaterer reiseplanen for familie Goderstad sin campingvognferie juli 2026. "
                "Endrer index.html, committer til git og pusher til "
                "https://github.com/arnego/sommerferie2026 (main branch). "
                "GitHub Pages publiserer siden automatisk på "
                "https://arnego.github.io/sommerferie2026/ etter ~30 sekunder. "
                "Brukes når noen vil endre rute, stopp, budsjett, huskeliste, "
                "datoer eller annet innhold i reiseplanen. "
                "Commit og push gjøres direkte uten å be om bekreftelse."
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
            name="read_travel_plan",
            description=(
                "Leser og returnerer en oppsummering av den nåværende reiseplanen "
                "fra ~/projects/sommerferie2026/index.html."
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
            text=(
                f"🌐 GitHub Pages: {PAGES_URL}\n"
                f"📦 GitHub repo: {GITHUB_REPO}"
            )
        )]

    if name == "read_travel_plan":
        try:
            html = read_html()
            mtime = datetime.fromtimestamp(
                INDEX_FILE.stat().st_mtime
            ).strftime("%d.%m.%Y %H:%M")
            return [types.TextContent(
                type="text",
                text=(
                    f"Reiseplanen er lastet ({len(html)} tegn). "
                    f"Sist endret: {mtime}.\n"
                    f"🌐 {PAGES_URL}\n"
                    f"📦 {GITHUB_REPO}"
                )
            )]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Feil: {e}")]

    if name == "update_travel_plan":
        instruction = arguments.get("instruction", "").strip()
        if not instruction:
            return [types.TextContent(
                type="text", text="Mangler instruksjon."
            )]

        # Bruk oppgitt commit-melding eller generer automatisk
        commit_message = arguments.get("commit_message", "").strip() or instruction

        try:
            current_html = read_html()
            updated_html = call_claude_for_update(instruction, current_html)

            if not updated_html.strip().startswith("<!"):
                return [types.TextContent(
                    type="text",
                    text="Feil: Fikk ikke gyldig HTML tilbake. Prøv igjen."
                )]

            write_html(updated_html)
            success, git_output = git_push(commit_message)

            if success:
                return [types.TextContent(
                    type="text",
                    text=(
                        f"✅ Reiseplanen er oppdatert og pushet til GitHub!\n"
                        f"📝 Commit: \"{commit_message[:72]}\"\n"
                        f"⏳ GitHub Pages oppdateres om ~30 sekunder.\n"
                        f"🌐 {PAGES_URL}"
                    )
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=(
                        f"⚠️ index.html er oppdatert lokalt, men git push feilet:\n"
                        f"{git_output[:300]}"
                    )
                )]

        except Exception as e:
            return [types.TextContent(type="text", text=f"❌ Feil: {e}")]

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
