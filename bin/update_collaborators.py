#!/usr/bin/env python3

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
META = ROOT / "_data" / "collaborators.yml"
STATS = ROOT / "_data" / "collaborator_stats.yml"

ALIASES = {
    "Tiznado Aitken, Ignacio": "Tiznado-Aitken, Ignacio",
    "Tiznado, Ignacio": "Tiznado-Aitken, Ignacio",
    "Aitken, Ignacio Tiznado": "Tiznado-Aitken, Ignacio",
    "Muñoz, JC": "Muñoz, Juan Carlos",
    "Munoz, Juan Carlos": "Muñoz, Juan Carlos",
    "Guzman, Luis A": "Guzmán, Luís Ángel",
    "Guzmán, Luís Ángel": "Guzmán, Luís Ángel",
    "Arellana, J": "Arellana, Julián",
    "Vecchio, G": "Vecchio, Giovanni",
    "Mora-Vega, Rodrigo": "Mora, Rodrigo",
    "Higgins, Christopher": "Higgins, Christopher D",
    "Silver, Michelle": "Silver, Michelle P",
    "Kelly, Noah": "Kelly, Noah Alexander",
    "Wong, Rachel": "Wong, Rachel K",
    "Yaksic, M": "Yaksic, Miguel",
    "Guimaraes, T": "Guimarães, Thiago",
    "Sánchez Lang, R": "Sánchez Lang, Ricardo",
    "Navas Duk, C": "Navas Duk, Cristian",
    "Páez, Antonio": "Páez, Antonio",
    "Paez, Antonio": "Páez, Antonio",
}

def extract_author_fields(text):
    fields = []
    pos = 0

    while True:
        match = re.search(r"\bauthor\s*=\s*\{", text[pos:], re.I)

        if not match:
            break

        start = pos + match.end()
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
    return [
        x.strip()
        for x in re.split(r"\s+and\s+", value)
        if x.strip() and x.strip().lower() != "others"
    ]


def normalize(name):
    name = " ".join(name.split())
    return ALIASES.get(name, name)


# --------------------------------------------------
# Extract collaborators from papers.bib
# --------------------------------------------------

text = BIB.read_text(encoding="utf-8")

authors = []

for field in extract_author_fields(text):
    authors.extend(split_authors(field))

collaborators = sorted({
    normalize(author)
    for author in authors
    if normalize(author) != "Tiznado-Aitken, Ignacio"
})


# --------------------------------------------------
# Load curated metadata
# --------------------------------------------------

metadata = yaml.safe_load(
    META.read_text(encoding="utf-8")
)

metadata_names = {
    person["name"]
    for person in metadata
}


# --------------------------------------------------
# Check for new collaborators
# --------------------------------------------------

missing = sorted(
    set(collaborators) - metadata_names
)

if missing:
    print("WARNING: New collaborators need metadata:")
    
    for name in missing:
        print(f"  - {name}")

    print(
        "\nAdd these people to _data/collaborators.yml "
        "before relying on the country/institution statistics."
    )


# --------------------------------------------------
# Calculate statistics from curated metadata
# --------------------------------------------------

countries = {
    person["country"]
    for person in metadata
    if person.get("country")
}

institutions = {
    person["institution"]
    for person in metadata
    if person.get("institution")
}

discipline_groups = {
    person["discipline_group"]
    for person in metadata
    if person.get("discipline_group")
}


stats = {
    "collaborators": len(collaborators),
    "institutions": len(institutions),
    "countries": len(countries),
    "discipline_groups": len(discipline_groups),
}


# --------------------------------------------------
# Write collaborator statistics
# --------------------------------------------------

STATS.write_text(
    yaml.safe_dump(
        stats,
        allow_unicode=True,
        sort_keys=False
    ),
    encoding="utf-8"
)

print("\nCollaborator statistics:")
print(f"  Collaborators: {stats['collaborators']}")
print(f"  Institutions:  {stats['institutions']}")
print(f"  Countries:     {stats['countries']}")
print(f"  Disciplines:   {stats['discipline_groups']}")
