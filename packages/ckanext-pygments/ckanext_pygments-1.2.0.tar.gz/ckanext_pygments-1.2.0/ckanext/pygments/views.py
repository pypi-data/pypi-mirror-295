from __future__ import annotations

import logging

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins as p
import ckan.plugins.toolkit as tk

import ckanext.pygments.cache as pygments_cache
import ckanext.pygments.config as pygment_config
import ckanext.pygments.utils as pygments_utils

log = logging.getLogger(__name__)
bp = Blueprint("pygments", __name__, url_prefix="/pygments")


@bp.route("/highlight/<resource_id>", methods=["GET"])
def highlight(resource_id: str) -> str:
    cache_manager = pygments_cache.RedisCache()
    cache_enabled = pygment_config.is_cache_enabled()
    preview = ""

    if cache_enabled:
        preview = cache_manager.get_data(resource_id)
        exceed_max_size = len(preview) > pygment_config.get_resource_cache_max_size()

        if exceed_max_size:
            cache_manager.invalidate(resource_id)

    if not preview:
        try:
            preview = pygments_utils.pygment_preview(
                resource_id,
                tk.request.args.get(
                    "theme", pygment_config.get_default_theme(), type=str
                ),
                tk.request.args.get(
                    "chunk_size", pygment_config.get_resource_cache_max_size(), type=int
                ),
            )
        except Exception as e:
            log.debug(
                "Pygments: failed to render preview: %s, resource_id: %s",
                e,
                resource_id,
            )
            preview = (
                "Pygments: Error rendering preview. Please, contact the administrator."
            )
        else:
            if cache_enabled and not exceed_max_size:
                cache_manager.set_data(resource_id, preview)

    return tk.render(
        "pygments/pygment_preview_body.html",
        {"preview": preview},
    )


if p.plugin_loaded("admin_panel"):
    from ckanext.ap_main.utils import ap_before_request
    from ckanext.ap_main.views.generics import ApConfigurationPageView

    pygments_admin = Blueprint("pygments_admin", __name__)
    pygments_admin.before_request(ap_before_request)

    class ConfigClearCacheView(MethodView):
        def post(self):
            pygments_cache.RedisCache.drop_cache()

            tk.h.flash_success(tk._("Cache has been cleared"))

            return tk.h.redirect_to("pygments_admin.config")

    pygments_admin.add_url_rule(
        "/admin-panel/pygments/clear-cache",
        view_func=ConfigClearCacheView.as_view("clear_cache"),
    )

    pygments_admin.add_url_rule(
        "/admin-panel/pygments/config",
        view_func=ApConfigurationPageView.as_view(
            "config",
            "pygments_config",
            render_template="pygments/config.html",
            page_title=tk._("Pygments config"),
        ),
    )
