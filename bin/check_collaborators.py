#!/usr/bin/env python3
"""
Check collaborator coverage and print network statistics.

Usage:
    python3 bin/check_collaborators.py

The script reads:
    _bibliography/papers.bib
    _data/collaborators.yml

It extracts author fields without requiring a BibTeX package, removes Ignacio,
applies the known name aliases below, and compares the resulting collaborators
against collaborators.yml.

It does NOT overwrite collaborators.yml.
"""

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
META = ROOT / "_data" / "collaborators.yml"

ALIASES = {
    "Tiznado Aitken, Ignacio": "Tiznado-Aitken, Ignacio",
    "Tiznado, Ignacio": "Tiznado-Aitken, Ignacio",
    "Aitken, Ignacio Tiznado": "Tiznado-Aitken, Ignacio",
    "Muñ{\\~n}oz, Juan Carlos": "Muñoz, Juan Carlos",
    "Mu{\\~n}oz, Juan Carlos": "Muñoz, Juan Carlos",
    "Munoz, Juan Carlos": "Muñoz, Juan Carlos",
    "Mu{\\~n}oz, JC": "Muñoz, Juan Carlos",
    "Muñoz, JC": "Muñoz, Juan Carlos",
    "Guzman, Luis A": "Guzmán, Luís Ángel",
    "Guzm{\\'a}n, Lu{\\'i}s {\\'A}ngel": "Guzmán, Luís Ángel",
    "Arellana, J": "Arellana, Julián",
    "Arellana, Juli{\\'a}n": "Arellana, Julián",
    "Vecchio, G": "Vecchio, Giovanni",
    "Mora-Vega, Rodrigo": "Mora, Rodrigo",
    "Mora, Rodrigo": "Mora, Rodrigo",
    "Higgins, Christopher": "Higgins, Christopher D",
    "Widener, Michael J": "Widener, Michael J",
    "Silver, Michelle P": "Silver, Michelle P",
    "Silver, Michelle": "Silver, Michelle P",
    "Kelly, Noah": "Kelly, Noah Alexander",
    "Wong, Rachel": "Wong, Rachel K",
    "Tiznado-Aitken, I": "Tiznado-Aitken, Ignacio",
    "Tiznado Aitken, I": "Tiznado-Aitken, Ignacio",
    "Hurtubia, RICARDO": "Hurtubia, Ricardo",
    "Mu{\\~n}oz, JC": "Muñoz, Juan Carlos",
    "Tironi, M": "Tironi, Martín",
    "Yaksic, M": "Yaksic, Miguel",
    "Guimaraes, T": "Guimarães, Thiago",
    "S{\\'a}nchez Lang, R": "Sánchez Lang, Ricardo",
    "Navas Duk, C": "Navas Duk, Cristian",
    "Batomen, Brice": "Batomen, Brice",
    "Paez, Antonio": "Páez, Antonio",
    "P{\\'a}ez, Antonio": "Páez, Antonio",
    "Jamal, Shaila": "Jamal, Shaila",
    "Smith Piel, Mar{\\'\\i}a Consuelo": "Smith Piel, María Consuelo",
    "Aitken, Ignacio Tiznado": "Tiznado-Aitken, Ignacio",
}

def extract_author_fields(text):
    fields = []
    pos = 0
    while True:
        m = re.search(r"\bauthor\s*=\s*\{", text[pos:], flags=re.I)
        if not m:
            break
        start = pos + m.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        fields.append(text[start:i-1])
        pos = i
    return fields

def split_authors(value):
    # Author separators are the literal " and " at brace depth zero.
    parts, start, depth, i = [], 0, 0, 0
    while i < len(value):
        ch = value[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if depth == 0 and value.startswith(" and ", i):
            parts.append(value[start:i].strip())
            i += 5
            start = i
            continue
        i += 1
    parts.append(value[start:].strip())
    return [p for p in parts if p and p.lower() != "others"]

def normalize(raw):
    raw = " ".join(raw.split())
    return ALIASES.get(raw, raw)

text = BIB.read_text(encoding="utf-8")
authors = []
for field in extract_author_fields(text):
    authors.extend(split_authors(field))

canonical = sorted({normalize(a) for a in authors
                    if normalize(a) != "Tiznado-Aitken, Ignacio"})

meta = yaml.safe_load(META.read_text(encoding="utf-8"))
meta_names = {x["name"] for x in meta}

print(f"Identifiable collaborators in papers.bib: {len(canonical)}")
print(f"Curated collaborators in collaborators.yml: {len(meta_names)}")
print()

missing = sorted(set(canonical) - meta_names)
unused = sorted(meta_names - set(canonical))

if missing:
    print("Authors found in papers.bib but not yet in collaborators.yml:")
    for x in missing:
        print(f"  - {x}")
else:
    print("Coverage: all extracted collaborators have metadata.")

if unused:
    print("\nMetadata entries not currently found in papers.bib:")
    for x in unused:
        print(f"  - {x}")

# Statistics from the curated metadata.
countries = {x["country"] for x in meta}
institutions = set()
for x in meta:
    # Split only explicit multiple-affiliation separators.
    for inst in re.split(r"\s*/\s*", x["institution"]):
        institutions.add(inst.strip())

groups = {x["discipline_group"] for x in meta}

print("\nCurated network statistics:")
print(f"  Collaborators: {len(meta)}")
print(f"  Countries:     {len(countries)}")
print(f"  Institutions:  {len(institutions)}")
print(f"  Disc. groups:  {len(groups)}")
