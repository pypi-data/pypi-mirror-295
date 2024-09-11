# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import os
import shutil

import pytest
from flask_webpackext.manifest import (
    JinjaManifest,
    JinjaManifestEntry,
    JinjaManifestLoader,
)
from invenio_access.permissions import system_identity
from invenio_app.factory import create_ui
from invenio_app_rdm.config import APP_RDM_ROUTES
from invenio_communities.communities.records.api import Community
from invenio_files_rest.models import Location
from invenio_rdm_records.records.api import RDMRecord
from invenio_search.proxies import current_search, current_search_client
from invenio_vocabularies.proxies import current_service as vocab_svc
from invenio_vocabularies.records.api import Vocabulary
from pytest_invenio.user import UserFixtureBase


#
# Mock the webpack manifest to avoid having to compile the full assets.
#
class MockJinjaManifest(JinjaManifest):
    """Mock manifest."""

    def __getitem__(self, key):
        """Get a manifest entry."""
        return JinjaManifestEntry(key, [key])

    def __getattr__(self, name):
        """Get a manifest entry."""
        return JinjaManifestEntry(name, [name])


class MockManifestLoader(JinjaManifestLoader):
    """Manifest loader creating a mocked manifest."""

    def load(self, filepath):
        """Load the manifest."""
        return MockJinjaManifest()


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Create test app."""
    return create_ui


@pytest.fixture(scope="module")
def app_config(app_config):
    """Testing configuration."""
    app_config["APP_RDM_DEPOSIT_FORM_TEMPLATE"] = "invenio_app_rdm/records/deposit.html"
    app_config["APP_RDM_ROUTES"] = APP_RDM_ROUTES
    app_config["DB_VERSIONING"] = False
    app_config["RDM_REQUESTS_ROUTES"] = {
        "user-dashboard-request-details": "/me/requests/<request_pid_value>",
        "community-dashboard-request-details": "/communities/<pid_value>/requests/<request_pid_value>",
        "community-dashboard-invitation-details": "/communities/<pid_value>/invitations/<request_pid_value>",
    }
    app_config["RECORDS_REFRESOLVER_CLS"] = (
        "invenio_records.resolver.InvenioRefResolver"
    )
    app_config["RECORDS_REFRESOLVER_STORE"] = (
        "invenio_jsonschemas.proxies.current_refresolver_store"
    )
    app_config["REQUESTS_FACETS"] = {}
    app_config["SECRET_KEY"] = "super_secret_key"
    app_config["SECURITY_PASSWORD_SALT"] = "test-secret-key"
    app_config["SQLALCHEMY_DATABASE_URI"] = (
        os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///"
    )
    app_config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app_config["TESTING"] = True
    app_config["WEBPACKEXT_MANIFEST_LOADER"] = MockManifestLoader

    return app_config


@pytest.fixture()
def user(app, db):
    """User creation and login fixture."""
    test_user = UserFixtureBase(
        email="user@example.org",
        password="super_secure_password",
        username="pytest_user",
    )
    test_user.create(app, db)
    test_user.app_login()
    return test_user


@pytest.fixture()
def vocabularies(db):
    """Creates db tables and fills specific vocabularies."""
    vocab_svc.create_type(system_identity, "resourcetypes", "rsrct")
    vocab_svc.create_type(system_identity, "subjects", "sub")
    vocab_svc.create_type(system_identity, "affiliations", "aff")
    vocab_svc.create_type(system_identity, "funders", "fun")
    vocab_svc.create_type(system_identity, "creatorsroles", "crr")
    vocab_svc.create_type(system_identity, "contributorsroles", "cor")
    vocab_svc.create_type(system_identity, "languages", "lng")
    vocab_svc.create_type(system_identity, "licenses", "lic")
    vocab_svc.create_type(system_identity, "descriptiontypes", "dty")
    vocab_svc.create_type(system_identity, "datetypes", "dat")
    vocab_svc.create_type(system_identity, "names", "names")
    vocab_svc.create_type(system_identity, "relationtypes", "rlt")
    vocab_svc.create_type(system_identity, "removalreasons", "rem")
    vocab_svc.create_type(system_identity, "titletypes", "ttyp")
    vocab_svc.create_type(system_identity, "communitytypes", "comtyp")
    vocab_svc.create_type(system_identity, "awards", "awa")

    vocab_svc.create(
        system_identity,
        {
            "id": "dataset",
            "icon": "table",
            "props": {
                "csl": "dataset",
                "datacite_general": "Dataset",
                "datacite_type": "",
                "openaire_resourceType": "21",
                "openaire_type": "dataset",
                "eurepo": "info:eu-repo/semantics/other",
                "schema.org": "https://schema.org/Dataset",
                "subtype": "",
                "type": "dataset",
                "marc21_type": "dataset",
                "marc21_subtype": "",
            },
            "title": {"en": "Dataset"},
            "tags": ["depositable", "linkable"],
            "type": "resourcetypes",
        },
    )


@pytest.fixture()
def search_indices():
    """Creates all registered Elasticsearch indexes."""
    to_create = [RDMRecord.index._name, Vocabulary.index._name, Community.index._name]
    # list to trigger iter
    list(current_search.create(ignore_existing=True, index_list=to_create))
    current_search_client.indices.refresh()
    return to_create


@pytest.fixture()
def files_loc(db):
    """Creates app location for testing."""
    loc_path = "testing_data_location"
    if os.path.exists(loc_path):
        shutil.rmtree(loc_path)

    os.makedirs(loc_path)
    loc = Location(name="local", uri=loc_path, default=True)
    db.session.add(loc)
    db.session.commit()
    return loc_path


@pytest.fixture()
def minimal_record():
    """Minimal record for creation during tests."""
    return {
        "access": {
            "record": "public",
            "files": "public",
        },
        "files": {
            "enabled": False,
        },
        "metadata": {
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Moser",
                        "given_name": "Maximilian",
                        "type": "personal",
                    }
                },
            ],
            "publication_date": "2024-06-21",
            "publisher": "TU Wien",
            "resource_type": {"id": "dataset"},
            "title": "Some test record",
        },
    }
