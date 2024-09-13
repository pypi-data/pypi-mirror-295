# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom overrides for search mappings."""

from pathlib import Path

from invenio_search import current_search


def override_mappings(app):
    """Override specific search mappings."""
    path = Path(__file__).parent

    # community members
    prefix, name = "communitymembers-members", "member-v1.0.0"
    current_search.mappings[f"{prefix}-{name}"] = str(path / f"{name}.json")

    # member invitations
    prefix, name = "communitymembers-archivedinvitations", "archivedinvitation-v1.0.0"
    current_search.mappings[f"{prefix}-{name}"] = str(path / f"{name}.json")
