# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from .policies import (
    TUWCommunityPermissionPolicy,
    TUWRecordPermissionPolicy,
    TUWRequestsPermissionPolicy,
)

__all__ = (
    "TUWCommunityPermissionPolicy",
    "TUWRecordPermissionPolicy",
    "TUWRequestsPermissionPolicy",
)
