from __future__ import annotations

from snowcli.cli.project.schemas.relaxed_map import RelaxedMap
from snowcli.cli.project.util import IDENTIFIER
from strictyaml import (
    Bool,
    EmptyList,
    MapPattern,
    Optional,
    Regex,
    Seq,
    Str,
)

Argument = RelaxedMap({"name": Str(), "type": Str()})

_callable_mapping = {
    "name": Regex(IDENTIFIER),
    "handler": Str(),
    "returns": Str(),
    "signature": Seq(Argument) | EmptyList(),
    Optional("runtime"): Str(),
    Optional("external_access_integration"): Seq(Str()),
    Optional("secrets"): MapPattern(Str(), Str()),
}

function_schema = RelaxedMap(_callable_mapping)

procedure_schema = RelaxedMap(
    {
        **_callable_mapping,
        Optional("execute_as_caller"): Bool(),
    }
)

snowpark_schema = RelaxedMap(
    {
        "project_name": Str(),
        "stage_name": Str(),
        "src": Str(),
        Optional("functions"): Seq(function_schema),
        Optional("procedures"): Seq(procedure_schema),
    }
)
