# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test routes."""


def test_frontpage(app):
    """Test the frontpage registered via our module."""
    app.config.update(
        {
            "THEME_SITENAME": "TUW Theme Testing",
        }
    )
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"TUW Theme Testing" in response.data


def test_tuw_policies_route(app):
    """Test the policies page registered via our module."""
    resp = app.test_client().get("/tuw/policies")
    assert resp.status_code == 200
    assert b"Policies" in resp.data


def test_tuw_contact_route(app):
    """Test the contact page registered via our module."""
    resp = app.test_client().get("/tuw/contact")
    assert resp.status_code == 200
    assert b"Contact" in resp.data


def test_tuwstone_florian_woerister(app):
    """Test Florian's tombstone page."""
    resp = app.test_client().get("/tuwstones/florian.woerister")
    assert resp.status_code == 200
    assert b"Florian W&ouml;rister" in resp.data
    assert b"Ex Almost TU:RD Manager" in resp.data
