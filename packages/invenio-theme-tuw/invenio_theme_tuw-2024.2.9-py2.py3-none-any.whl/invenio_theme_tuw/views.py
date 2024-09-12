# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""TU Wien theme for Invenio (RDM)."""

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_limiter import Limiter
from flask_login import current_user, login_required
from invenio_accounts.models import User
from invenio_accounts.proxies import current_datastore
from invenio_app.limiter import useragent_and_ip_limit_key
from invenio_app_rdm.records_ui.views.deposits import deposit_create, deposit_edit
from invenio_base.utils import obj_or_import_string
from invenio_communities.proxies import current_communities
from invenio_communities.views.communities import communities_new
from invenio_db import db
from invenio_mail.tasks import send_email
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_rdm_records.proxies import current_rdm_records_service as rec_service
from invenio_rdm_records.resources.serializers import (
    SchemaorgJSONLDSerializer,
    UIJSONSerializer,
)
from sqlalchemy.exc import NoResultFound

from .search import FrontpageRecordsSearch


def _get_limiter(app):
    """Get the configured limiter, or initialize it if not available."""
    limiter = app.extensions["invenio-app"].limiter
    if limiter is None:
        limiter = Limiter(
            app,
            key_func=obj_or_import_string(
                app.config.get("RATELIMIT_KEY_FUNC"), default=useragent_and_ip_limit_key
            ),
        )

    return limiter


@login_required
def guarded_deposit_create(*args, **kwargs):
    """Guard the creation page for records, based on permissions."""
    if not rec_service.check_permission(g.identity, "create"):
        return (
            render_template("invenio_theme_tuw/guards/deposit.html", user=current_user),
            403,
        )

    return deposit_create(*args, **kwargs)


@login_required
def guarded_deposit_edit(*args, **kwargs):
    """Guard the edit page for records, based on permissions."""
    # NOTE: this extra loading of the draft introduces an extra DB query, but i think
    #       it should not make too much of a difference for us
    try:
        draft = rec_service.draft_cls.pid.resolve(
            kwargs["pid_value"], registered_only=False
        )
    except (PIDDoesNotExistError, NoResultFound):
        return render_template(current_app.config["THEME_404_TEMPLATE"]), 404

    if not rec_service.check_permission(g.identity, "update_draft", record=draft):
        if not rec_service.check_permission(g.identity, "preview", record=draft):
            return (
                render_template(
                    "invenio_theme_tuw/guards/deposit.html", user=current_user
                ),
                403,
            )
        else:
            # if the user has permission to preview the draft but not to edit it,
            # redirect them to the preview page
            return redirect(
                url_for(
                    "invenio_app_rdm_records.record_detail",
                    pid_value=draft.pid.pid_value,
                    preview=1,
                )
            )

    return deposit_edit(*args, **kwargs)


@login_required
def guarded_communities_create(*args, **kwargs):
    """Guard the communities creation page, based on permissions."""
    if not current_communities.service.check_permission(g.identity, "create"):
        return (
            render_template(
                "invenio_theme_tuw/guards/community.html", user=current_user
            ),
            403,
        )

    return communities_new(*args, **kwargs)


def resolve_record(recid):
    """Resolve the record with the given recid into an API class object."""
    try:
        return rec_service.record_cls.pid.resolve(recid, registered_only=False)
    except NoResultFound:
        # if no record can be found for the ID, let's try if we can find a draft
        # (e.g. in the case of a draft preview)
        #
        # note: `invenio_pidstore.errors` contains further exceptions that could
        #       be raised during the PID resolution
        return rec_service.draft_cls.pid.resolve(recid, registered_only=False)


def resolve_user_owner(record):
    """Resolve the first user-type owner of the record.

    The record is expected to be an API-class object, and the result will be a User
    model object.
    """
    owner = record.parent.access.owner
    if not owner or owner.owner_type != "user":
        return None

    return owner.resolve()


def get_name_of_user_owner(owner):
    """Resolve the user referenced by the owner object and get their full name."""
    user_id = owner["user"]
    return User.query.get(user_id).user_profile.get("full_name")


def _fetch_user_infos():
    """Fetch information about each user for our hacky user info list."""
    user_infos = []
    trusted_user_role = current_datastore.find_role("trusted-user")

    for user in db.session.query(User).order_by(User.id).all():
        # check if the user has given us consent for record curation
        curation_consent = (user.preferences or {}).get("curation_consent", False)

        # check if the user can upload datasets
        trusted = user.has_role(trusted_user_role)

        info = {
            "user": user,
            "tiss_id": (user.user_profile or {}).get("tiss_id", None),
            "curation_consent": curation_consent,
            "trusted": trusted,
        }

        user_infos.append(info)

    return user_infos


def _toggle_user_trust(user_id):
    """Add the "trusted-user" role to the user or remove it."""
    trusted_user_role = current_datastore.find_role("trusted-user")
    user = current_datastore.find_user(id=user_id)

    if not user.has_role(trusted_user_role):
        current_datastore.add_role_to_user(user, trusted_user_role)
        verb = "Trusted"
    else:
        current_datastore.remove_role_from_user(user, trusted_user_role)
        verb = "Untrusted"

    db.session.commit()
    user_name = user.user_profile.get("full_name") if user.user_profile else "N/A"
    return f"{verb} user #{user_id} ({user_name or 'N/A'})"


def create_blueprint(app):
    """Create a blueprint with routes and resources."""
    blueprint = Blueprint(
        "invenio_theme_tuw",
        __name__,
        template_folder="theme/templates",
        static_folder="theme/static",
    )

    @blueprint.app_template_filter("tuw_doi_identifier")
    def tuw_doi_identifier(identifiers):
        """Extract DOI from sequence of identifiers."""
        if identifiers is not None:
            for identifier in identifiers:
                if identifier.get("scheme") == "doi":
                    return identifier.get("identifier")

    @blueprint.app_template_global("tuw_create_schemaorg_metadata")
    def tuw_create_schemaorg_metadata(record):
        """Create schema.org metadata to include in a <script> tag."""
        return SchemaorgJSONLDSerializer().serialize_object(record)

    @blueprint.app_template_global("record_count")
    def record_count():
        try:
            return FrontpageRecordsSearch().count()
        except Exception:
            return "all"

    @blueprint.route("/")
    def tuw_index():
        """Custom landing page showing the latest 5 records."""
        try:
            records = FrontpageRecordsSearch()[:5].sort("-created").execute()
        except Exception:
            records = []

        return render_template(
            "invenio_theme_tuw/overrides/frontpage.html",
            records=_records_serializer(records),
        )

    def _records_serializer(records=None):
        """Serialize list of records."""
        record_list = []
        for record in records or []:
            record_list.append(UIJSONSerializer().dump_obj(record.to_dict()))
        return record_list

    @blueprint.route("/tuw/contact-uploader/<recid>", methods=["GET", "POST"])
    def contact_uploader(recid):
        """Contact page for the contact's uploader."""
        captcha = current_app.extensions["invenio-theme-tuw"].captcha
        record = resolve_record(recid)
        form_values = request.form.to_dict()
        if current_user and not current_user.is_anonymous:
            form_values.setdefault("name", current_user.user_profile.get("full_name"))
            form_values.setdefault("email", current_user.email)

        if record is None:
            abort(404)

        owner = record.parent.access.owned_by
        if not owner:
            abort(404)

        owner = owner.resolve()

        submitted = False
        captcha_failed = False
        if request.method == "POST":
            # NOTE: the captcha is a simple spam prevention measure, and it also
            #       prevents the form from being accidentally resubmitted wia refresh
            if not current_app.config["CAPTCHA_ENABLE"] or captcha.validate():
                sitename = current_app.config["THEME_SITENAME"]
                sender_name = request.form["name"]
                sender_email = request.form["email"]
                inquiry = request.form["message"] or "<Empty Message>"
                html_message = render_template(
                    "invenio_theme_tuw/contact_mail_html.jinja",
                    sender_name=sender_name,
                    sender_email=sender_email,
                    message=inquiry,
                    uploader=owner,
                    record=record,
                )
                message = render_template(
                    "invenio_theme_tuw/contact_mail_text.jinja",
                    sender_name=sender_name,
                    sender_email=sender_email,
                    message=inquiry,
                    uploader=owner,
                    record=record,
                )

                add_sender_to_cc = current_app.config.get(
                    "THEME_TUW_CONTACT_UPLOADER_ADD_EMAIL_TO_CC", False
                )
                record_title = record.metadata["title"]
                send_email(
                    {
                        "subject": f'{sitename}: Inquiry about your record "{record_title}" from {sender_name}',
                        "html": html_message,
                        "body": message,
                        "recipients": [owner.email],
                        "cc": [sender_email] if add_sender_to_cc else [],
                        "reply_to": sender_email,
                    }
                )

                submitted = True

            else:
                captcha_failed = True

        response = render_template(
            "invenio_theme_tuw/contact_uploader.html",
            uploader=owner,
            submitted=submitted,
            record=record,
            captcha_failed=captcha_failed,
            form_values=form_values,
        )
        return response, 200 if not captcha_failed else 428

    @blueprint.route("/tuw/policies")
    def tuw_policies():
        """Page showing the available repository policies."""
        return render_template("invenio_theme_tuw/policies.html")

    @blueprint.route("/tuw/terms-of-use")
    def tuw_terms_of_use():
        """Page showing the repository's terms of use documents."""
        return render_template("invenio_theme_tuw/terms_of_use.html")

    @blueprint.route("/tuw/contact")
    def tuw_contact():
        """Contact page."""
        return render_template("invenio_theme_tuw/contact.html")

    @blueprint.route("/tuw/admin/users", methods=["GET", "POST"])
    def list_user_info():
        """Hacky endpoint for listing user information."""
        admin_role = current_datastore.find_role("admin")
        if current_user and current_user.has_role(admin_role):

            # handle trusting of user
            if request.method == "POST":
                if (user_id := request.form.get("user_id", None)) is not None:
                    try:
                        flash(_toggle_user_trust(user_id))
                    except Exception as e:
                        flash(e)

            return render_template(
                "invenio_theme_tuw/users_infos.html",
                user_infos=_fetch_user_infos(),
            )
        else:
            abort(403)

    @blueprint.route("/tuw/admin/users/welcome")
    def show_user_welcome_text():
        """Show the welcome text for new users, to be sent to them via email."""
        admin_role = current_datastore.find_role("admin")
        if current_user and current_user.has_role(admin_role):
            uid = request.args.get("uid", None)

            if user := current_datastore.get_user(uid):
                return render_template(
                    "invenio_theme_tuw/users_welcome.html",
                    user=user,
                )
            else:
                # if the user can't be found, redirect to the overview
                return redirect(url_for(".list_user_info"))

        else:
            abort(403)

    @blueprint.route("/tuwstones/florian.woerister")
    def tuw_tombstone_florian():
        """Tombstone page for Florian Wörister."""
        return render_template("invenio_theme_tuw/tuwstones/florian_woerister.html")

    # register filters for showing uploaders
    blueprint.add_app_template_filter(resolve_record)
    blueprint.add_app_template_filter(resolve_user_owner)

    return blueprint


def override_deposit_pages(app):
    """Override the existing view functions with more access control."""
    # we have some additional role-based permissions (trusted-user) that decide
    # among other things if people can create records/drafts
    # this is not considered in the original view functions, which is why we
    # currently need to wrap them with our own guards
    app.view_functions["invenio_app_rdm_records.deposit_edit"] = guarded_deposit_edit
    app.view_functions["invenio_app_rdm_records.deposit_create"] = (
        guarded_deposit_create
    )
    app.view_functions["invenio_communities.communities_new"] = (
        guarded_communities_create
    )

    # limit the amount of contact requests that can be made per time period
    # (this needs to be done after the Flask-Limiter extension has been init.)
    if (limiter := _get_limiter(app)) is not None:
        limit_value = app.config.get("THEME_TUW_CONTACT_UPLOADER_RATE_LIMIT", "5/hour")
        contact_uploader_view_func = app.view_functions[
            "invenio_theme_tuw.contact_uploader"
        ]
        app.view_functions["invenio_theme_tuw.contact_uploader"] = limiter.limit(
            limit_value, methods=["POST"]
        )(contact_uploader_view_func)
