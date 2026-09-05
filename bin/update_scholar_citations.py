#!/usr/bin/env python

import os
import sys
import yaml
from datetime import datetime
from scholarly import scholarly


def load_scholar_user_id() -> str:
    """Load the Google Scholar user ID from the configuration file."""
    config_file = "_data/socials.yml"

    if not os.path.exists(config_file):
        print(
            f"Configuration file {config_file} not found. "
            "Please ensure the file exists and contains your Google Scholar user ID."
        )
        sys.exit(1)

    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        scholar_user_id = config.get("scholar_userid")

        if not scholar_user_id:
            print(
                "No 'scholar_userid' found in the configuration file. "
                "Please add 'scholar_userid' to _data/socials.yml."
            )
            sys.exit(1)

        return scholar_user_id

    except yaml.YAMLError as e:
        print(
            f"Error parsing YAML file {config_file}: {e}. "
            "Please check the file for correct YAML syntax."
        )
        sys.exit(1)


SCHOLAR_USER_ID = load_scholar_user_id()
OUTPUT_FILE = "_data/citations.yml"


def get_scholar_citations() -> None:
    """Fetch and update Google Scholar citation data."""

    print(f"Fetching citations for Google Scholar ID: {SCHOLAR_USER_ID}")

    today = datetime.now().strftime("%Y-%m-%d")

    existing_data = {}

    # Check whether the output file already exists
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r") as f:
                existing_data = yaml.safe_load(f) or {}

            if (
                existing_data
                and "metadata" in existing_data
                and "last_updated" in existing_data["metadata"]
            ):
                print(
                    f"Last updated on: "
                    f"{existing_data['metadata']['last_updated']}"
                )

                if existing_data["metadata"]["last_updated"] == today:
                    print(
                        "Citations data is already up-to-date. "
                        "Skipping fetch."
                    )
                    return

        except Exception as e:
            print(
                f"Warning: Could not read existing citation data from "
                f"{OUTPUT_FILE}: {e}"
            )

    scholarly.set_timeout(15)
    scholarly.set_retries(3)

    try:
        author = scholarly.search_author_id(SCHOLAR_USER_ID)
        author_data = scholarly.fill(author)

    except Exception as e:
        print(
            f"Error fetching author data from Google Scholar for user ID "
            f"'{SCHOLAR_USER_ID}': {e}. "
            "Please check your internet connection and Scholar user ID."
        )
        sys.exit(1)

    if not author_data:
        print(
            f"Could not fetch author data for user ID "
            f"'{SCHOLAR_USER_ID}'."
        )
        sys.exit(1)

    if "publications" not in author_data:
        print(
            f"No publications found in author data for user ID "
            f"'{SCHOLAR_USER_ID}'."
        )
        sys.exit(1)

    citation_data = {
        "metadata": {
            "last_updated": today
        },
        "papers": {},
        "annual_citations": {}
    }

    # ---------------------------------------------------------
    # Individual publication citation counts
    # ---------------------------------------------------------

    for pub in author_data["publications"]:

        try:
            pub_id = pub.get("pub_id") or pub.get("author_pub_id")

            if not pub_id:
                print(
                    f"Warning: No ID found for publication: "
                    f"{pub.get('bib', {}).get('title', 'Unknown')}. "
                    "This publication will be skipped."
                )
                continue

            title = pub.get("bib", {}).get(
                "title",
                "Unknown Title"
            )

            year = pub.get("bib", {}).get(
                "pub_year",
                "Unknown Year"
            )

            citations = pub.get(
                "num_citations",
                0
            )

            print(
                f"Found: {title} ({year}) - "
                f"Citations: {citations}"
            )

            citation_data["papers"][pub_id] = {
                "title": title,
                "year": year,
                "citations": citations,
            }

        except Exception as e:
            print(
                f"Error processing publication "
                f"'{pub.get('bib', {}).get('title', 'Unknown')}': {e}. "
                "This publication will be skipped."
            )

    # ---------------------------------------------------------
    # Google Scholar annual citation history
    # ---------------------------------------------------------

    cites_per_year = author_data.get("cites_per_year", {})

    if cites_per_year:
        citation_data["annual_citations"] = {
            str(year): int(citations)
            for year, citations in sorted(
                cites_per_year.items(),
                key=lambda item: int(item[0])
            )
        }

        print("\nAnnual citations:")

        for year, citations in citation_data["annual_citations"].items():
            print(f"  {year}: {citations}")

    else:
        print(
            "Warning: Google Scholar did not return "
            "annual citation data."
        )

    # ---------------------------------------------------------
    # Write citation data
    # ---------------------------------------------------------

    try:
        with open(OUTPUT_FILE, "w") as f:
            yaml.dump(
                citation_data,
                f,
                width=1000,
                sort_keys=False
            )

        print(f"\nCitation data saved to {OUTPUT_FILE}")

    except Exception as e:
        print(
            f"Error writing citation data to {OUTPUT_FILE}: {e}. "
            "Please check file permissions and disk space."
        )
        sys.exit(1)


if __name__ == "__main__":
    try:
        get_scholar_citations()

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)