import functools
import os
from typing import Dict, List, Tuple, Type, Union

import click
import tomli


class RepoType(click.types.StringParamType):
    name = "repo_url_trim"


def get_color(text: str, color: str) -> str:
    return click.style(str(text), fg=color)


def get_passed_params(ctx: click.Context) -> Dict:
    return {
        k: v
        for k, v in ctx.params.items()
        if ctx.get_parameter_source(k) == click.core.ParameterSource.COMMANDLINE
    }


def get_toml_config(defaults: Dict) -> Dict:
    try:
        with open(os.path.join(os.getcwd(), "pyproject.toml"), "rb") as f:
            toml_dict: Dict = tomli.load(f)
        return {**defaults, **toml_dict["tool"]["pre-commit-update"]}
    except (FileNotFoundError, KeyError):
        return defaults


def get_dict_diffs(d1: Dict, d2: Dict) -> Dict:
    return {k: d2[k] for k in d2 if d2[k] != d1[k]}


def get_converted_iterable(
    iterable: Union[List, Tuple], _type: Union[Type[List], Type[Tuple]]
) -> Union[Tuple, List]:
    return (
        _type(map(functools.partial(get_converted_iterable, _type=_type), iterable))
        if isinstance(iterable, (list, tuple))
        else iterable
    )


def get_converted_dict_values(d: Dict) -> Dict:
    for k, v in d.items():
        d[k] = get_converted_iterable(v, list) if isinstance(v, tuple) else v
    return d
