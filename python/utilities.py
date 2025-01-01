'''
title: utilities.py
author: Samuel J. Huskey (with assistance from Chat-GPT 4o)

Purpose: Helper functions for use in multiple Jupyter notebooks 
in this repository
'''

import re
import unicodedata

def normalize_author_name(name):
    """Normalize author names for consistent matching."""
    # Decompose Unicode characters
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    # Convert to lowercase, strip whitespace, and remove non-alphanumeric characters (except spaces)
    normalized_name = re.sub(r"[^\w\s]", "", name.lower().strip())
    return re.sub(r"\s+", " ", normalized_name)  # Normalize multiple spaces

def prepare_dicts(authors,works):
    """Process author dataframe and works dataframe"""
    # Prepare the lookup dictionary of variant author names
    variant_to_authorized = {
        normalize_author_name(row["variant_name"]): {
            "authorized_name": row["authorized_name"], 
            "author_id": row["dll_id_author"]
        }
        for _, row in authors.iterrows()
    }

    # Prepare the lookup dictionary for titles
    title_to_work = {
        row["title"]: {
            "dll_id_work": row["dll_id_work"],
            "dll_id_author": row["dll_id_author"]
        }
        for _, row in works.iterrows()
    }

    return variant_to_authorized, title_to_work, 