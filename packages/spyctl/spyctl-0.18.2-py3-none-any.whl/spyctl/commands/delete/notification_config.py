"""Handles the delete notification config command"""

from typing import List

import click

import spyctl.commands.delete.shared_options as _so
import spyctl.config.configs as cfg
import spyctl.spyctl_lib as lib
from spyctl import cli
from spyctl.api.notifications import (
    get_notification_policy,
    put_notification_policy,
)


@click.command(
    "notification-config", cls=lib.CustomCommand, epilog=lib.SUB_EPILOG
)
@_so.delete_options
def delete_notif_cfg_cmd(name_or_id, yes=False):
    """Delete a notification config by name or uid"""
    if yes:
        cli.set_yes_option()
    handle_delete_notif_config(name_or_id)


def handle_delete_notif_config(name_or_id):
    """Delete a notification config by name or uid"""
    ctx = cfg.get_current_context()
    notif_pol = get_notification_policy(*ctx.get_api_data())
    routes: List = notif_pol.get(lib.ROUTES_FIELD, [])
    del_index = None
    del_id = None
    for i, route in enumerate(routes):
        cfg_id = route.get(lib.DATA_FIELD, {}).get(lib.ID_FIELD)
        name = route.get(lib.DATA_FIELD, {}).get(lib.NAME_FIELD)
        if name_or_id in [cfg_id, name]:
            if del_index is not None and name == name_or_id:
                cli.err_exit(f"{name_or_id} is ambiguous, use ID")
            del_index = i
            del_id = cfg_id
    if del_index is None:
        cli.err_exit(f"No notification config matching '{name_or_id}'")
    if cli.query_yes_no(
        f"Are you sure you want to delete notification config {del_id}"
    ):
        routes.pop(del_index)
        notif_pol[lib.ROUTES_FIELD] = routes
        put_notification_policy(*ctx.get_api_data(), notif_pol)
        cli.try_log(f"Successfully deleted notification config '{del_id}'")
