"""Handles the get notification config templates command."""

import fnmatch
from typing import List

import click

import spyctl.commands.get.shared_options as _so
import spyctl.resources as _r
import spyctl.spyctl_lib as lib
from spyctl import cli
from spyctl.commands.get import get_lib


@click.command(
    "notification-config-templates",
    cls=lib.CustomCommand,
    epilog=lib.SUB_EPILOG,
)
@_so.help_option
@_so.name_or_id_arg
@_so.exact_match_option
@_so.output_option
@click.option(
    "--type",
    metavar="",
    type=click.Choice(lib.NOTIF_TMPL_TYPES),
    help="Emit the full organization notification policy"
    " object when using yaml or json output format.",
)
def get_notification_config_templates_cmd(name_or_id, output, **filters):
    """Get notification config templates by name or id."""
    get_lib.output_time_log(
        lib.NOTIFICATION_CONFIG_TEMPLATES_RESOURCE.name_plural, 0, 0
    )
    exact = filters.pop("exact")
    name_or_id = get_lib.wildcard_name_or_id(name_or_id, exact)
    filters = {
        key: value for key, value in filters.items() if value is not None
    }
    handle_get_notification_config_templates(name_or_id, output)


def handle_get_notification_config_templates(name_or_id, output, **filters):
    """Output notification config templates by name or id."""
    tmpl_type = filters.pop(lib.TYPE_FIELD, None)
    templates: List[_r.notification_configs.NotificationConfigTemplate] = []
    if not name_or_id:
        templates.extend(_r.notification_configs.NOTIF_CONFIG_TEMPLATES)
    else:
        for tmpl in _r.notification_configs.NOTIF_CONFIG_TEMPLATES:
            if fnmatch.fnmatch(
                tmpl.display_name, name_or_id
            ) or tmpl.id == name_or_id.strip("*"):
                templates.append(tmpl)
    if tmpl_type:
        templates = [
            tmpl
            for tmpl in templates
            if tmpl.type == lib.NOTIF_TMPL_MAP.get(tmpl_type)
        ]
    if output in [lib.OUTPUT_DEFAULT, lib.OUTPUT_WIDE]:
        summary = _r.notification_configs.notif_config_tmpl_summary_output(
            templates
        )
        cli.show(summary, lib.OUTPUT_RAW)
    else:
        for tmpl in templates:
            cli.show(tmpl.as_dict(), output)
