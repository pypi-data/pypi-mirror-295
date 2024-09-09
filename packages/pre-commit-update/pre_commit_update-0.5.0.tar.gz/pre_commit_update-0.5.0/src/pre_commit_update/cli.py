import os
import sys
from typing import Any, Dict, Optional, Tuple

import click

from .managers import (
    EnvManager,
    MessageManager,
    OptionManager,
    RepoManager,
    YAMLManager,
)
from .utils import (
    RepoType,
    get_color,
    get_converted_dict_values,
    get_dict_diffs,
    get_passed_params,
    get_toml_config,
)


def _preview(
    *, defaults: Dict, toml_params: Dict, cmd_params: Dict, final_params: Dict
) -> None:
    click.echo(get_color("Default configuration values:", "blue"))
    for k, v in defaults.items():
        click.echo(f"{k} = {v}")
    click.echo(
        get_color("\npyproject.toml configuration values (difference):", "yellow")
    )
    toml_diff: Dict = get_dict_diffs(defaults, toml_params)
    if toml_diff:
        for k, v in toml_diff.items():
            click.echo(f"{k} = {v}")
    else:
        click.echo("Same as the default configuration / no configuration found")
    click.echo(get_color("\nCommand line configuration values (difference):", "red"))
    cmd_diff: Dict = get_dict_diffs(toml_params, cmd_params)
    if cmd_diff:
        for k, v in cmd_diff.items():
            click.echo(f"{k} = {v}")
    else:
        click.echo("Same as the default configuration / pyproject.toml configuration")
    click.echo(get_color("\nFinal configuration values:", "green"))
    for k, v in final_params.items():
        click.echo(f"{k} = {v}")


def _run(
    *,
    dry_run: bool,
    all_versions: bool,
    verbose: bool,
    warnings: bool,
    jobs: Optional[int],
    exclude: Tuple,
    keep: Tuple,
    bleeding_edge: Tuple,
    tag_prefix: Tuple,
) -> None:
    # Backup and set needed env variables
    env_manager: EnvManager = EnvManager()
    env_manager.setup()
    # Do the magic
    try:
        message_manager: MessageManager = MessageManager()
        yaml_manager: YAMLManager = YAMLManager(
            os.path.join(os.getcwd(), ".pre-commit-config.yaml")
        )
        option_manager: OptionManager = OptionManager(
            warnings,
            all_versions,
            exclude,
            keep,
            bleeding_edge,
            tag_prefix,
            set(
                [
                    repo["repo"].split("/")[-1]
                    for repo in yaml_manager.data["repos"]
                    if repo["repo"].startswith("http")
                ]
            ),
        )
        option_manager.validate(message_manager)
        repo_manager: RepoManager = RepoManager(
            yaml_manager.data["repos"],
            all_versions,
            jobs,
            option_manager.exclude,
            option_manager.keep,
            option_manager.bleeding_edge,
            option_manager.tag_prefix,
        )
        repo_manager.get_updates(message_manager)

        if warnings and message_manager.warning:
            message_manager.output_messages(message_manager.warning)

        if verbose:
            for output in (
                message_manager.no_update,
                message_manager.excluded,
                message_manager.kept,
            ):
                if not output:
                    continue
                message_manager.output_messages(output)

        if message_manager.to_update:
            message_manager.output_messages(message_manager.to_update)

            if dry_run:
                raise click.ClickException(get_color("Changes detected", "red"))

            yaml_manager.data["repos"] = repo_manager.repos_data
            yaml_manager.dump()
            click.echo(get_color("Changes detected and applied", "green"))
            return

        click.echo(get_color("No changes detected", "green"))

    except Exception as ex:
        sys.exit(str(ex))

    finally:
        # Restore env variables
        env_manager.restore()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-d/-nd",
    "--dry-run/--no-dry-run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Checks for the new versions without updating if enabled",
)
@click.option(
    "-a/-na",
    "--all-versions/--no-all-versions",
    is_flag=True,
    show_default=True,
    default=False,
    help="Includes the alpha/beta versions when updating if enabled",
)
@click.option(
    "-v/-nv",
    "--verbose/--no-verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Displays the complete update output if enabled",
)
@click.option(
    "-w/-nw",
    "--warnings/--no-warnings",
    is_flag=True,
    show_default=True,
    default=True,
    help="Displays warning messages if enabled",
)
@click.option(
    "-p/-np",
    "--preview/--no-preview",
    is_flag=True,
    show_default=True,
    default=False,
    help="Previews the cli option values by the overwriting order if enabled (disables the actual cli work!)",
)
@click.option(
    "-j",
    "--jobs",
    type=int,
    show_default=True,
    default=None,
    help="Maximum number of worker threads to be used for processing",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    type=RepoType(),
    default=(),
    help="Exclude specific repo(s) by the REPO_URL_TRIM - use '*' as a wildcard",
)
@click.option(
    "-k",
    "--keep",
    multiple=True,
    type=RepoType(),
    default=(),
    help="Keep the version of specific repo(s) by the REPO_URL_TRIM (still checks for the new versions) - use '*' as a wildcard",
)
@click.option(
    "-b",
    "--bleeding-edge",
    multiple=True,
    type=RepoType(),
    default=(),
    help="Get the latest version or commit of specific repo(s) by the REPO_URL_TRIM - use '*' as a wildcard",
)
@click.option(
    "-t",
    "--tag-prefix",
    multiple=True,
    type=(RepoType(), str),
    default=(),
    help="Set the custom tag prefix for the specific repo(s) by combining REPO_URL_TRIM with tag prefix value",
)
@click.pass_context
def cli(ctx: click.Context, **_: Any):
    defaults: Dict = {
        p.name: list(p.default) if isinstance(p.default, tuple) else p.default
        for p in ctx.command.params
    }
    toml_params: Dict = get_toml_config(defaults)
    cmd_params: Dict = get_passed_params(ctx)
    final_params: Dict = {**toml_params, **cmd_params}

    if final_params.pop("preview"):
        _preview(
            defaults=get_converted_dict_values(defaults),
            toml_params=get_converted_dict_values(toml_params),
            cmd_params=get_converted_dict_values(cmd_params),
            final_params=get_converted_dict_values(final_params),
        )
        return

    _run(**final_params)


if __name__ == "__main__":
    cli()
