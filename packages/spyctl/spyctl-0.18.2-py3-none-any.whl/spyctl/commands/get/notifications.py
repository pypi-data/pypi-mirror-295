"""Handles retrieval of notification_configs."""

import fnmatch
from typing import Dict

import click

import spyctl.commands.get.shared_options as _so
import spyctl.config.configs as cfg
import spyctl.filter_resource as filt
import spyctl.resources as _r
import spyctl.spyctl_lib as lib
from spyctl import cli
from spyctl.api.notifications import get_notification_policy
from spyctl.commands.get import get_lib


@click.command(
    "notification-configs", cls=lib.CustomCommand, epilog=lib.SUB_EPILOG
)
@_so.help_option
@_so.name_or_id_arg
@_so.output_option
def get_notification_configs(name_or_id, output):
    """Get notification_configs by name or id."""
    get_lib.output_time_log(
        lib.NOTIFICATION_CONFIGS_RESOURCE.name_plural, 0, 0
    )
    handle_get_notification_configs(name_or_id, output)


def handle_get_notification_configs(name_or_id, output):
    """Output notification_configs by name or id."""
    ctx = cfg.get_current_context()
    n_pol = get_notification_policy(*ctx.get_api_data())
    if n_pol is None or not isinstance(n_pol, dict):
        cli.err_exit("Could not load notification policy")
    routes = n_pol.get(lib.ROUTES_FIELD, [])
    if name_or_id:
        routes = filt.filter_obj(routes, ["data.id", "data.name"], name_or_id)
    get_lib.show_get_data(
        routes,
        output,
        lambda data: _r.notification_configs.notifications_summary_output(
            data, lib.NOTIF_TYPE_ALL
        ),
        lambda data: _r.notification_configs.notifications_wide_output(
            data, lib.NOTIF_TYPE_ALL
        ),
    )


@click.command(
    "notification-targets", cls=lib.CustomCommand, epilog=lib.SUB_EPILOG
)
@_so.help_option
@_so.name_or_id_arg
@_so.output_option
def get_notification_targets(name_or_id, output):
    """Get notification_targets by name or id."""
    handle_get_notification_targets(name_or_id, output)


def handle_get_notification_targets(name_or_id, output):
    """Output notification_targets by name or id."""
    get_lib.output_time_log(
        lib.NOTIFICATION_TARGETS_RESOURCE.name_plural, 0, 0
    )
    ctx = cfg.get_current_context()
    n_pol = get_notification_policy(*ctx.get_api_data())
    if n_pol is None or not isinstance(n_pol, dict):
        cli.err_exit("Could not load notification targets")
    targets: Dict = n_pol.get(lib.TARGETS_FIELD, {})
    if name_or_id:
        tmp_tgts = {}
        for tgt_name, tgt_data in targets.items():
            tgt_obj = _r.notification_targets.Target(
                backend_target={tgt_name: tgt_data}
            )
            if tgt_obj.id == name_or_id.strip("*") or fnmatch.fnmatch(
                tgt_name, name_or_id
            ):
                tmp_tgts[tgt_name] = tgt_data
        targets = tmp_tgts
    get_lib.show_get_data(
        targets,
        output,
        _r.notification_targets.targets_summary_output,
        _r.notification_targets.targets_wide_output,
    )
