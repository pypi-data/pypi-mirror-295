"""Handles the delete notification target command"""

from typing import Dict

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
    "notification-target", cls=lib.CustomCommand, epilog=lib.SUB_EPILOG
)
@_so.delete_options
def delete_notif_tgt_cmd(name_or_id, yes=False):
    """Delete a notification target by name or uid"""
    if yes:
        cli.set_yes_option()
    handle_delete_notif_tgt(name_or_id)


def handle_delete_notif_tgt(name_or_id):
    ctx = cfg.get_current_context()
    notif_pol = get_notification_policy(*ctx.get_api_data())
    targets: Dict = notif_pol.get(lib.TARGETS_FIELD, {})
    del_name = None
    # check if name exists
    if name_or_id in targets:
        del_name = name_or_id
    if not del_name:
        for tgt_name, tgt in targets.items():
            tgt_id = tgt.get(lib.DATA_FIELD, {}).get(lib.ID_FIELD)
            if tgt_id is None:
                continue
            if tgt_id == name_or_id:
                del_name = tgt_name
    if not del_name:
        cli.err_exit(f"No notification target matching '{name_or_id}'.")
    if cli.query_yes_no(
        "Are you sure you want to delete notification target" f" '{del_name}'?"
    ):
        notif_pol = get_notification_policy(*ctx.get_api_data())
        notif_pol[lib.TARGETS_FIELD].pop(del_name)
        put_notification_policy(*ctx.get_api_data(), notif_pol)
        cli.try_log(f"Successfully deleted notification target '{del_name}'")
