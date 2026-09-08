#!/usr/bin/env python3

from pathlib import Path
import re
import unicodedata
import yaml

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "_bibliography" / "papers.bib"
META = ROOT / "_data" / "collaborators.yml"
STATS = ROOT / "_data" / "collaborator_stats.yml"


# --------------------------------------------------
# Known BibTeX name variants
# --------------------------------------------------

ALIASES = {
    
    "Berr{\\'\\i}os, Emilio": "Emilio Berríos",
    "Guzman, LA": "Luis Ángel Guzmán",
    "Larra{\\'\\i}n, Clemente": "Clemente Larraín",
    "Lyeo, Joonsoo S": "Joonsoo Lyeo",
    "Parga, Jo{\\~a}o Pedro Figueira Amorim": "João Pedro Figueira Amorim Parga",
    "Riva, Myl{\\`e}ne": "Mylène Riva",
    "Tironi, Mart{\\'\\i}n": "Martín Tironi",
    
    # Ignacio
    "Tiznado Aitken, Ignacio": "Ignacio Tiznado-Aitken",
    "Tiznado, Ignacio": "Ignacio Tiznado-Aitken",
    "Aitken, Ignacio Tiznado": "Ignacio Tiznado-Aitken",
    "Tiznado-Aitken, I": "Ignacio Tiznado-Aitken",
    "Tiznado Aitken, I": "Ignacio Tiznado-Aitken",
    "Aitken, Ignacio Tiznado": "Ignacio Tiznado-Aitken",

    # Muñoz
    "Muñoz, Juan Carlos": "Juan Carlos Muñoz",
    "Munoz, Juan Carlos": "Juan Carlos Muñoz",
    "Muñoz, JC": "Juan Carlos Muñoz",
    "Mu{\\~n}oz, Juan Carlos": "Juan Carlos Muñoz",
    "Mu{\\~n}oz, JC": "Juan Carlos Muñoz",

    # Guzmán
    "Guzman, Luis A": "Luis Ángel Guzmán",
    "Guzmán, Luís Ángel": "Luis Ángel Guzmán",
    "Guzm{\\'a}n, Lu{\\'i}s {\\'A}ngel": "Luis Ángel Guzmán",

    # Arellana
    "Arellana, J": "Julián Arellana",
    "Arellana, Juli{\\'a}n": "Julián Arellana",

    # Vecchio
    "Vecchio, G": "Giovanni Vecchio",

    # Mora
    "Mora-Vega, Rodrigo": "Rodrigo Mora",
    "Mora, Rodrigo": "Rodrigo Mora",

    # Higgins
    "Higgins, Christopher": "Christopher D. Higgins",
    "Higgins, Christopher D": "Christopher D. Higgins",

    # Widener
    "Widener, Michael": "Michael J. Widener",
    "Widener, Michael J": "Michael J. Widener",

    # Silver
    "Silver, Michelle": "Michelle P. Silver",
    "Silver, Michelle P": "Michelle P. Silver",

    # Kelly
    "Kelly, Noah": "Noah Alexander Kelly",
    "Kelly, Noah Alexander": "Noah Alexander Kelly",

    # Wong
    "Wong, Rachel": "Rachel K. Wong",
    "Wong, Rachel K": "Rachel K. Wong",

    # Yaksic
    "Yaksic, M": "Miguel Yaksic",

    # Guimarães
    "Guimaraes, T": "Thiago Guimarães",

    # Sánchez Lang
    "Sánchez Lang, R": "Ricardo Sánchez Lang",
    "S{\\'a}nchez Lang, R": "Ricardo Sánchez Lang",

    # Navas Duk
    "Navas Duk, C": "Cristian Navas Duk",

    # Páez
    "Paez, Antonio": "Antonio Páez",
    "Páez, Antonio": "Antonio Páez",
    "P{\\'a}ez, Antonio": "Antonio Páez",

    # Tironi
    "Tironi, M": "Martín Tironi",

    # Carrasco etc.
    "Batomen, Brice": "Brice Batomen Kuimi",

    # Ricardo Hurtubia
    "Hurtubia, RICARDO": "Ricardo Hurtubia",
    "Hurtubia, Ricardo": "Ricardo Hurtubia",

    # Smith Piel
    "Smith Piel, María Consuelo": "María Consuelo Smith Piel",
    "Smith Piel, Mar{\\'\\i}a Consuelo": "María Consuelo Smith Piel",
}


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def clean_latex(text):
    """
    Convert common LaTeX accent encodings to Unicode.
    """
    replacements = {
        r"{\'a}": "á",
        r"{\'e}": "é",
        r"{\'i}": "í",
        r"{\'o}": "ó",
        r"{\'u}": "ú",
        r"{\\'a}": "á",
        r"{\\'e}": "é",
        r"{\\'i}": "í",
        r"{\\'o}": "ó",
        r"{\\'u}": "ú",
        r"{\\~n}": "ñ",
        r"{\\~a}": "ã",
        r"{\\~o}": "õ",
        r"{\\`e}": "è",
        r"{\\`a}": "à",
        r"{\\'\\i}": "í",
        r"{\\~\\i}": "ĩ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove remaining braces used only for BibTeX grouping
    text = text.replace("{", "").replace("}", "")

    return text


def normalize_text(text):
    """
    Normalize spelling for comparison:
    - lowercase
    - remove accents
    - remove punctuation
    - collapse whitespace
    """
    text = clean_latex(text)
    text = text.lower()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def name_key(name):
    """
    Convert a person's name into an order-independent comparison key.

    This allows:
        Ricardo Hurtubia
        Hurtubia, Ricardo

    to be treated as the same person.
    """
    name = clean_latex(name)
    name = " ".join(name.split())

    if "," in name:
        surname, given = name.split(",", 1)
        parts = normalize_text(given).split() + normalize_text(surname).split()
    else:
        parts = normalize_text(name).split()

    return " ".join(sorted(parts))


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

        fields.append(text[start:i - 1])
        pos = i

    return fields


def split_authors(value):
    return [
        x.strip()
        for x in re.split(r"\s+and\s+", value)
        if x.strip() and x.strip().lower() != "others"
    ]


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

# Create lookup by normalized name
metadata_lookup = {
    name_key(name): name
    for name in metadata_names
}


# --------------------------------------------------
# Extract authors from papers.bib
# --------------------------------------------------

text = BIB.read_text(encoding="utf-8")

authors = []

for field in extract_author_fields(text):
    authors.extend(split_authors(field))


# --------------------------------------------------
# Match BibTeX names to curated collaborators
# --------------------------------------------------

matched_collaborators = set()
unmatched = set()

for raw_name in authors:

    # Remove Ignacio
    normalized_raw = normalize_text(raw_name)

    if "tiznado" in normalized_raw:
        continue

    # Explicit alias
    if raw_name in ALIASES:
        display_name = ALIASES[raw_name]

        if display_name in metadata_names:
            matched_collaborators.add(display_name)
        else:
            unmatched.add(raw_name)

        continue

    # General order-independent match
    key = name_key(raw_name)

    if key in metadata_lookup:
        matched_collaborators.add(metadata_lookup[key])
    else:
        unmatched.add(raw_name)


# --------------------------------------------------
# Report unmatched names
# --------------------------------------------------

if unmatched:
    print("\nWARNING: These BibTeX names could not be matched")
    print("to the curated collaborators.yml list:\n")

    for name in sorted(unmatched):
        print(f"  - {name}")

    print(
        "\nThese should be reviewed before they are treated "
        "as new collaborators.\n"
    )


# --------------------------------------------------
# Calculate statistics
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
    "collaborators": len(matched_collaborators),
    "institutions": len(institutions),
    "countries": len(countries),
    "discipline_groups": len(discipline_groups),
}


# --------------------------------------------------
# Write statistics
# --------------------------------------------------

STATS.write_text(
    yaml.safe_dump(
        stats,
        allow_unicode=True,
        sort_keys=False
    ),
    encoding="utf-8"
)


# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\nCollaborator statistics:")
print(f"  Collaborators: {stats['collaborators']}")
print(f"  Institutions:  {stats['institutions']}")
print(f"  Countries:     {stats['countries']}")
print(f"  Disciplines:   {stats['discipline_groups']}")
