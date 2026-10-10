#!/usr/bin/env python3
"""
Verifica di governance del Travel-Vault. Da lanciare dopo ogni modifica,
con qualsiasi harness (opencode, Claude Code, Codex, Cursor, ...):

    python3 _AI/scripts/vault_check.py

Controlli (ERRORE = exit code 1, AVVISO = solo segnalazione):
  1. Frontmatter YAML presente nelle note attive
  2. Wikilink [[...]] risolvibili nelle note attive
  3. Privacy: le note sensibili hanno `publish: false`; blocchi
     <!-- private --> / <!-- /private --> bilanciati
  4. Fonte unica: i file di istruzioni agente non duplicano lo stato
     delle prenotazioni (va solo in Info/Japan/Lista Prenotazioni.md)
  5. Nessun percorso assoluto (es. C:\\...) nei file per agenti
  6. `last_updated` nel formato YYYY-MM-DD
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".obsidian", "node_modules", "_website", "_private"}

# Note "attive": devono avere frontmatter e link validi
ACTIVE = [
    "Info",
    "Itinerari/Japan/2026",
    "_AI/knowledge",
]

# Note che non devono MAI finire sul sito pubblico
PRIVATE_REQUIRED = [
    "Info/Japan/Allergie Alimentari Rebecca.md",
    "Info/Japan/Assicurazione Heymondo.md",
    "Info/Japan/Spese Reali.md",
    "Info/Japan/Lista Prenotazioni.md",
    "Info/Japan/Voli/Prenotazione China Eastern (09-08-26).md",
]
# Categorie frontmatter sensibili: ogni nota con queste categorie va privata
PRIVATE_CATEGORIES = {"allergie", "assicurazione", "spese", "prenotazioni", "voli-prenotati", "documenti"}
# Cartelle i cui file vanno privati (alloggi prenotati); i file elencati sono eccezioni pubbliche
PRIVATE_DIRS = {"Locations/Japan/Hotels": {"Hotel-Hostel-Case-Appartamenti.md"}}

# File di istruzioni agente: niente stato prenotazioni duplicato, niente path assoluti
AGENT_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    ".agents/skills/travel-vault-agent/SKILL.md",
    "_AI/INDEX.md",
    "_AI/README.md",
    "_AI/knowledge/workspace.md",
    "opencode.jsonc",
]
STATUS_RE = re.compile(r"(❌|✅|🔵)[^\n]{0,40}\b(prenotat|da prenotare|acquistat)", re.I)
ABS_PATH_RE = re.compile(r"\b[A-Za-z]:\\\\?[A-Za-z]")

errors: list[str] = []
warnings: list[str] = []


def rel(p: Path) -> str:
    return p.relative_to(VAULT).as_posix()


def md_files(base: Path):
    for p in sorted(base.rglob("*.md")):
        if not SKIP_DIRS.intersection(p.relative_to(VAULT).parts):
            yield p


def frontmatter(text: str) -> str | None:
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    return m.group(1) if m else None


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


# Indice dei nomi file (Obsidian risolve i wikilink per basename)
names: set[str] = set()
for p in VAULT.rglob("*"):
    if p.is_file() and not SKIP_DIRS.intersection(p.relative_to(VAULT).parts):
        names.add(p.name.lower())
        names.add(p.stem.lower())

# 1-2. Frontmatter + wikilink nelle note attive
active_files = [p for d in ACTIVE for p in md_files(VAULT / d)]
for p in active_files:
    text = p.read_text(encoding="utf-8", errors="replace")
    if frontmatter(text) is None:
        errors.append(f"[frontmatter] manca in {rel(p)}")
    for m in re.finditer(r"\[\[([^\]|#^]+)", strip_code(text)):
        target = m.group(1).strip().rstrip("\\").split("/")[-1].lower()
        if target and target not in names and Path(target).stem not in names:
            errors.append(f"[wikilink] [[{m.group(1).strip()}]] non trovato in {rel(p)}")

# 3. Privacy
def is_private(p: Path) -> bool:
    fm = frontmatter(p.read_text(encoding="utf-8", errors="replace")) or ""
    return re.search(r"^publish:\s*[\"']?false[\"']?\s*$", fm, re.M) is not None

for f in PRIVATE_REQUIRED:
    p = VAULT / f
    if not p.exists():
        warnings.append(f"[privacy] file atteso non trovato: {f} (aggiornare PRIVATE_REQUIRED)")
    elif not is_private(p):
        errors.append(f"[privacy] {f} deve avere `publish: false`")

for p in md_files(VAULT / "Info"):
    fm = frontmatter(p.read_text(encoding="utf-8", errors="replace")) or ""
    m = re.search(r"^category:\s*[\"']?([\w-]+)", fm, re.M)
    if m and m.group(1).lower() in PRIVATE_CATEGORIES and not is_private(p):
        errors.append(f"[privacy] {rel(p)} ha category '{m.group(1)}' ma non `publish: false`")

for d, public in PRIVATE_DIRS.items():
    for p in md_files(VAULT / d):
        if p.name not in public and not is_private(p):
            errors.append(f"[privacy] {rel(p)} (alloggio prenotato) deve avere `publish: false`")

for p in md_files(VAULT):
    text = p.read_text(encoding="utf-8", errors="replace")
    o = len(re.findall(r"<!--\s*private\s*-->", text, re.I))
    c = len(re.findall(r"<!--\s*/private\s*-->", text, re.I))
    if o != c:
        errors.append(f"[privacy] blocchi private sbilanciati in {rel(p)} ({o} aperti, {c} chiusi)")

# 4-5. File per agenti
for f in AGENT_FILES:
    p = VAULT / f
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    for n, line in enumerate(text.splitlines(), 1):
        if STATUS_RE.search(line) and "fonte di verit" not in line.lower():
            errors.append(f"[fonte-unica] {f}:{n} duplica lo stato prenotazioni → spostarlo in Info/Japan/Lista Prenotazioni.md")
        if ABS_PATH_RE.search(line):
            errors.append(f"[portabilita] {f}:{n} contiene un percorso assoluto → usare percorsi relativi alla root")

# 6. last_updated
for p in active_files:
    fm = frontmatter(p.read_text(encoding="utf-8", errors="replace")) or ""
    m = re.search(r"^last_updated:\s*[\"']?([^\"'\s]+)", fm, re.M)
    if m and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(1)):
        warnings.append(f"[metadati] last_updated non ISO in {rel(p)}: {m.group(1)}")

for w in warnings:
    print("AVVISO ", w)
for e in errors:
    print("ERRORE ", e)
print(f"\nvault_check: {len(active_files)} note attive · {len(errors)} errori · {len(warnings)} avvisi")
sys.exit(1 if errors else 0)
