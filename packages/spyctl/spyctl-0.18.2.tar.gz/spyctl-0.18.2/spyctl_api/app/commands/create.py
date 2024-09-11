from dataclasses import dataclass, field

import spyctl.commands.create.create_cmd_group as spyctl_create
import spyctl.spyctl_lib as lib
from fastapi import HTTPException
from typing import List, Dict


from app import app_lib

# ------------------------------------------------------------------------------
# Create Suppression Policy
# ------------------------------------------------------------------------------


@dataclass
class CreateSuppressionPolicyInput:
    type: str
    obj_uid: str = ""
    auto_generate_user_scope: bool = False
    name: str = ""
    org_uid: str = ""
    api_key: str = ""
    api_url: str = ""
    selectors: dict = field(default_factory=dict)


@dataclass
class CreateSuppressionPolicyOutput:
    policy: dict


def suppression_policy(
    i: CreateSuppressionPolicyInput,
) -> CreateSuppressionPolicyOutput:
    if i.type == lib.POL_TYPE_TRACE:
        return trace_suppression_policy(i)
    raise HTTPException(
        status_code=400,
        detail="Bad Request. Invalid suppression policy type.",
    )


def trace_suppression_policy(
    i: CreateSuppressionPolicyInput,
) -> CreateSuppressionPolicyOutput:
    spyctl_ctx = app_lib.generate_spyctl_context(
        i.org_uid, i.api_key, i.api_url
    )
    pol = spyctl_create.create_trace_suppression_policy(
        i.obj_uid,
        i.auto_generate_user_scope,
        i.name,
        ctx=spyctl_ctx,
        **i.selectors,
    )
    output = CreateSuppressionPolicyOutput(pol.as_dict())
    return output


# ------------------------------------------------------------------------------
# Create Guardian Policy
# ------------------------------------------------------------------------------


@dataclass
class CreateGuardianPolicyInput:
    name: str = ""
    input_objs: List[Dict] = field(default_factory=[])
    mode: str = lib.POL_MODE_AUDIT
    org_uid: str = ""
    api_key: str = ""
    api_url: str = ""


@dataclass
class CreateGuardianPolicyOutput:
    policy: dict


def guardian_policy(
    i: CreateGuardianPolicyInput,
) -> CreateGuardianPolicyOutput:
    spyctl_ctx = app_lib.generate_spyctl_context(
        i.org_uid, i.api_key, i.api_url
    )
    pol = spyctl_create.create_guardian_policy_from_json(
        i.name, i.mode, i.input_objs, spyctl_ctx
    )
    output = CreateGuardianPolicyOutput(pol)
    return output
