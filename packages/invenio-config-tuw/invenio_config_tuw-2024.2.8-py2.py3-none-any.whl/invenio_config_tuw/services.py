# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Overrides for core services."""

from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.services.components import DefaultRecordsComponents


class ParentAccessSettingsComponent(ServiceComponent):
    """Service component that allows access requests per default."""

    def create(self, identity, record, **kwargs):
        """Set the parent access settings to allow access requests."""
        settings = record.parent.access.settings
        settings.allow_guest_requests = True
        settings.allow_user_requests = True
        settings.secret_link_expiration = 30


TUWRecordsComponents = [
    *DefaultRecordsComponents,
    ParentAccessSettingsComponent,
]
