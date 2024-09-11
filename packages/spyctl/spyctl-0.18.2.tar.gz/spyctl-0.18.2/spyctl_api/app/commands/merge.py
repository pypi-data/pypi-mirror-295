from dataclasses import dataclass
from typing import Dict, List

from spyctl.commands.merge import merge_resource

from app import app_lib
import app.exceptions as ex

# ------------------------------------------------------------------------------
# Merge Object(s) into Object
# ------------------------------------------------------------------------------


@dataclass
class MergeInput:
    object: Dict
    merge_objects: List[Dict]
    org_uid: str = ""
    api_key: str = ""
    api_url: str = ""


@dataclass
class MergeOutput:
    merged_object: str


def merge(i: MergeInput) -> MergeOutput:
    spyctl_ctx = app_lib.generate_spyctl_context(
        i.org_uid, i.api_key, i.api_url
    )
    merged_object = merge_resource(
        i.object,
        "API Merge Request Object",
        i.merge_objects,
        ctx=spyctl_ctx,
    )
    if not merged_object:
        msg = app_lib.flush_spyctl_log_messages()
        ex.internal_server_error(msg)
    merged_object = merged_object[0]
    app_lib.flush_spyctl_log_messages()
    return MergeOutput(merged_object.get_obj_data())
