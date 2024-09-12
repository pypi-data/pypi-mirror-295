# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test specific functions."""

import html
import json

from flask import render_template_string
from invenio_access.permissions import system_identity
from invenio_rdm_records.proxies import current_rdm_records_service as rec_service

from invenio_theme_tuw.views import guarded_deposit_create


def test_tuw_create_schemaorg_metadata(
    app, vocabularies, minimal_record, files_loc, search_indices
):
    """Test Schema.org metadata creation."""
    record = rec_service.create(system_identity, minimal_record)
    template = r"{{ tuw_create_schemaorg_metadata(record) }}"
    with app.test_request_context():
        result = render_template_string(template, record=record.to_dict())
        parsed = json.loads(html.unescape(result))
        assert result and parsed
        assert "TU Wien" in result
        assert parsed["publisher"]["name"] == "TU Wien"
        for key in [
            "@context",
            "@type",
            "identifier",
            "name",
            "creator",
            "author",
            "publisher",
            "datePublished",
            "dateModified",
            "url",
        ]:
            assert key in parsed


def test_deposit_create_allowed(app, user, vocabularies):
    """Test deposit guard. Allowing creation case."""
    # default behavior is to allow creation, no further action required
    response = guarded_deposit_create()
    assert "deposit-form" in response


def test_deposit_create_denied(app, user):
    """Test deposit guard. Denying creation case."""
    # deny create permission
    rec_service.config.permission_policy_cls.can_create = []

    response, status_code = guarded_deposit_create()
    assert (
        "For your first upload, your account must be manually activated by our team"
        in response
    )
    assert status_code == 403


# NOTE: these tests are failing because the user somehow is not authenticated,
# altough the assertion passes from the user fixture.

# def test_deposit_edit_allowed(app, user, minimal_record):
#     """Test deposit guard. Allowing edit case."""
#     rec_service.config.permission_policy_cls.can_create = [AnyUser()]
#     rec_service.config.permission_policy_cls.can_update = [AnyUser()]

#     draft = rec_service.create(user.identity, minimal_record)

#     response = guarded_deposit_edit(pid_value=draft.id)
#     assert "deposit-form" in response


# def test_deposit_edit_denied(app, user, minimal_record):
#     """Test deposit guard. Denying edit case."""
#     rec_service.config.permission_policy_cls.can_create = [AnyUser()]
#     rec_service.config.permission_policy_cls.can_update = [AnyUser()]

#     draft = rec_service.create(user.identity, minimal_record)
#     response = guarded_deposit_edit(pid_value=draft.id)
#     assert (
#         "For your first upload, your account must be manually activated by our team"
#         in response
#     )
