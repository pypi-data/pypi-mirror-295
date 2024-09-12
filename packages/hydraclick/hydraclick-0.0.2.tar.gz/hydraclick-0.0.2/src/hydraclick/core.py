import functools
import logging
import sys
from pathlib import Path
from typing import Callable, Any

import hydra
from omegaconf import DictConfig, OmegaConf
from unittest.mock import patch
import flogging

from hydraclick.display_config import display_config
from hydraclick.options import (
    hydra_args_argument,
    hydra_help_option,
    version_option,
    show_config_option,
    resolve_option,
    package_option,
    info_option,
    run_option,
    multirun_option,
    config_path_option,
    config_dir_option,
    config_name_option,
    shell_completion_option,
)

_logger = logging.getLogger(__name__)


def wrap_kwargs_and_config(
    function: Callable,
    run_mode: str = "config",  # "config" | "kwargs"
    print_config: bool = True,
    preprocess_config: Callable[[DictConfig], DictConfig] | None = None,
    resolve: bool = True,
):
    """Wrap a function to run as a hydra command."""

    @functools.wraps(function)
    def wrapper(config):
        if preprocess_config:
            config = preprocess_config(config)
        if isinstance(config, DictConfig) and resolve:
            try:
                OmegaConf.resolve(config)
            except Exception as e:
                display_config(config, logger=_logger)
                raise e
        if print_config:
            display_config(config, logger=_logger)
        if run_mode == "config":
            return function(config)
        return function(**config)

    return wrapper


def build_hydra_args(
    hydra_help: bool,
    version: bool,
    show_config: str,
    resolve: bool,
    package: str,
    info: bool,
    run: bool,
    multirun: bool,
    config_path: str,
    config_name: str,
    config_dir: str,
    shell_completion: bool,
    hydra_args: tuple[str, ...] | None = None,
) -> tuple[str, ...]:
    """Compose the arguments for the hydra command."""
    _logger.debug(f"Hydra args: {hydra_args}")
    hydra_args_ = []
    if hydra_help:
        hydra_args_.append("--hydra-help")
    if version:
        hydra_args_.append("--version")
    if show_config:
        hydra_args_.extend(("--cfg", show_config))
    if resolve:
        hydra_args_.append("--resolve")
    if package:
        hydra_args_.extend(("--package", f"{package}"))
    if info:
        hydra_args_.append("--info")
    if run:
        hydra_args_.append("--run")
    if multirun:
        hydra_args_.append("--multirun")
    if config_path:
        hydra_args_.extend(("--config-path", f"{config_path}"))
    if config_name:
        hydra_args_.extend(("--config-name", f"{config_name}"))
    if config_dir:
        hydra_args_.extend(("--config-dir", f"{config_dir}"))
    if shell_completion:
        hydra_args_.append("--shell-completion")
    _logger.debug(f"Hydra args after composition: {hydra_args}")
    return (*hydra_args_, *hydra_args)


def get_default_dir() -> str:
    """Get the default directory for the hydra config."""
    curr_dir = Path().cwd()
    # if there is a `config` folder inside curr_dir, return its path, otherwise return curr_dir
    return str(curr_dir / "config") if (curr_dir / "config").exists() else str(curr_dir)


def run_hydra(function: Callable, hydra_args: tuple[str, ...]) -> None:
    """Run a function as a hydra app."""

    @hydra.main(config_path=get_default_dir(), config_name="config", version_base=None)
    @functools.wraps(function)
    def _run_hydra_function(loaded_config: DictConfig):
        flogging.setup(allow_trailing_dot=True)
        return function(loaded_config)

    with patch("sys.argv", [sys.argv[0], *list(hydra_args)]):
        return _run_hydra_function()


def command_api(
    function: Callable[[DictConfig], Any],
    run_mode="config",
    preprocess_config=None,
    print_config=True,
    resolve=True,
) -> Callable:
    """Implement using click the hydra CLI API."""

    @hydra_args_argument
    @hydra_help_option
    @version_option
    @show_config_option
    @resolve_option
    @package_option
    @info_option
    @run_option
    @multirun_option
    @config_path_option
    @config_name_option
    @config_dir_option
    @shell_completion_option
    @functools.wraps(function)
    def click_compatible(
        hydra_help: bool,
        version: bool,
        show_config: str,
        resolve_: bool,
        package: str,
        info: bool,
        run: bool,
        multirun: bool,
        config_path: str,
        config_name: str,
        config_dir: str,
        shell_completion: bool,
        hydra_args: tuple[str, ...] | None = None,
    ):
        nonlocal print_config, run_mode, preprocess_config, resolve
        if show_config:
            print_config = False
        true_func = wrap_kwargs_and_config(
            function, run_mode, print_config, preprocess_config, resolve
        )
        hydra_args = build_hydra_args(
            hydra_help,
            version,
            show_config,
            resolve_,
            package,
            info,
            run,
            multirun,
            config_path,
            config_name,
            config_dir,
            shell_completion,
            hydra_args,
        )
        return run_hydra(true_func, hydra_args)

    return click_compatible


def hydra_command(
    run_mode: str = "config",  # "config" | "kwargs"
    print_config: bool = True,
    preprocess_config: Callable[[DictConfig], DictConfig] | None = None,
    resolve: bool = True,
):
    """Wrap a function so it can run as a hydra command."""

    def decorator(function: Callable):
        return command_api(
            function,
            run_mode=run_mode,
            print_config=print_config,
            preprocess_config=preprocess_config,
            resolve=resolve,
        )

    return decorator
