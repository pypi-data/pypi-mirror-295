import click


hydra_args_argument = click.argument("hydra_args", nargs=-1, type=click.UNPROCESSED)


# Information about hydra
hydra_help_option = click.option(
    "--hydra-help",
    "hydra_help",
    help="Shows Hydra specific flags",
    is_flag=True,
    default=False,
)

version_option = click.option(
    "--version",
    "version",
    help="Show Hydra's version and exit",
    is_flag=True,
    default=False,
)

# Debugging assistance
show_config_option = click.option(
    "--cfg",
    "-c",
    "show_config",
    help="Show config instead of running. Takes as parameter one of job, hydra or all",
    type=click.Choice(["job", "hydra", "all"]),
    default=None,
)
resolve_option = click.option(
    "--resolve",
    "resolve_",
    help=(
        "Used in conjunction with the --cfg flag; "
        "resolve interpolations in the config before printing it"
    ),
    is_flag=True,
    default=False,
)
package_option = click.option(
    "--package",
    "-p",
    "package",
    help="Used in conjunction with --cfg to select a specific config package to show",
    type=click.STRING,
)
info_option = click.option(
    "--info",
    "-i",
    "info",
    help=(
        "Print Hydra information. This includes installed plugins, "
        "Config Search Path, Defaults List, generated config and more"
    ),
    is_flag=True,
    default=False,
)
# Running Hydra applications:
run_option = click.option(
    "--run",
    "run",
    help="Run is the default mode and is not normally needed.",
    is_flag=True,
    default=False,
)
multirun_option = click.option(
    "--multirun",
    "-m",
    "multirun",
    help="Run multiple jobs with the configured launcher and sweeper",
    is_flag=True,
    default=False,
)
config_path_option = click.option(
    "--config-path",
    "-cp",
    "config_path",
    help=(
        "Overrides the config_path specified in hydra.main(). "
        "The config_path is absolute or relative to the Python file declaring @hydra.main()."
    ),
    default=None,
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=None,
    ),
)
config_name_option = click.option(
    "--config-name",
    "-cn",
    "config_name",
    help="Overrides the config_name specified in hydra.main()",
    default=None,
    type=click.STRING,
)
config_dir_option = click.option(
    "--config-dir",
    "-cd",
    "config_dir",
    help=(
        "Adds an additional config directory to the config search path. "
        "This is useful for installed apps that want to allow their users"
        " to provide additional configs"
    ),
    default=None,
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=None,
    ),
)
shell_completion_option = click.option(
    "--shell-completion",
    "-sc",
    "shell_completion",
    help="Install or Uninstall shell tab completion",
    is_flag=True,
    default=False,
)
# Unused stuff
parallel_option = click.option(
    "--parallel",
    "-p",
    "parallel",
    help="Run each shard and configuration sweep in parallel",
    is_flag=True,
    default=False,
)
num_shards_option = click.option(
    "--num-shards",
    "-n",
    help="Number of shards to split the data processing",
    default=0,
)

file_option = click.option(
    "--file",
    "-f",
    "file",
    help="Path to the configuration file",
    default=None,
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=None,
    ),
)
