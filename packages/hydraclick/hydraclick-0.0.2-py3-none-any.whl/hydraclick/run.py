from functools import partial
from pathlib import Path
import logging
import sys
from typing import Callable, Any

import hydra
from omegaconf import DictConfig
from unittest.mock import patch
import flogging

from hydraclick.display_config import display_config

_logger = logging.getLogger(__name__)


def get_hydra_configs(
    config_file: Path | str,
    hydra_args: tuple[str, ...],
) -> list[DictConfig]:
    """Load the necessary configuration for running click commands from a config.yaml file.

    Args:
        config_file: Path to the target config.yaml file. If None, the default \
            config file is loaded.
        hydra_args: Arguments passed to hydra for composing the project configuration.

    Returns:
        configs: list of all the resolved configurations specified by the command arguments.

    """
    config_file = Path(config_file)
    configs = []
    if config_file.exists() and config_file.is_file():
        _logger.info("Loading config file from %s", config_file)
        hydra_args = ["--config-dir", str(config_file.parent), *list(hydra_args)]  # type: ignore

        @hydra.main(
            config_path=str(config_file.parent), config_name=config_file.stem, version_base=None
        )
        def load_config(loaded_config: DictConfig):
            flogging.setup(allow_trailing_dot=True)
            nonlocal configs
            configs.append(loaded_config)

        with patch("sys.argv", [sys.argv[0], *list(hydra_args)]):
            load_config()

    else:
        _logger.error(f"Invalid config file path provided: {config_file}")
        msg = f"Invalid config file: {config_file}"
        raise ValueError(msg)
    return configs


def _run_sequential(
    function: Callable[[DictConfig], Any],
    configs: list[DictConfig],
    num_shards: int = 0,
) -> int:
    """Run the sweep sequentially."""
    for config in configs:
        if num_shards == 0:
            function(config)
            continue
        if num_shards > 0:
            config["num_shards"] = num_shards
        num_shards = config.get("num_shards", 1)
        for shard_ix in range(num_shards):
            config["shard_ix"] = shard_ix
            _logger.info("Running shard %d", shard_ix)
            function(config)
    return 0


def _run_parallel(
    function: Callable[[DictConfig], Any],
    configs: list[DictConfig],
    num_shards: int = 0,
) -> int:
    """Run the sweep sequentially."""
    try:
        import ray  # noqa: PLC0415
    except ImportError:
        _logger.error("Ray is not installed. Please install it with `pip install ray`")
        return 1
    _conf = configs[0]
    ray_opts = _conf.get("ray", {})
    ray_opts["ignore_reinit_error"] = True
    _logger.info("Launching ray with parameters: %s", ray_opts)
    ray.init(**ray_opts)
    run_remote = ray.remote(function)
    requests = []
    _logger.info("Ray launched successfully")
    for config in configs:
        if num_shards == 0:
            req_id = run_remote.remote(config)
            requests.append(req_id)
            continue
        if num_shards > 0:
            config["num_shards"] = num_shards
        num_shards = config.get("num_shards", 1)
        for shard_ix in range(num_shards):
            config["shard_ix"] = shard_ix
            req_id = run_remote.remote(config)
            _logger.info("Running shard %d", shard_ix)
            requests.append(req_id)
    ray.get(requests)
    return 0


def run_function(
    function: Callable[[DictConfig], Any],
    config_file: str | Path | None = None,
    hydra_args: tuple[str, ...] | None = None,
    multirun: bool = True,
    parallel: bool = False,
    num_shards: int = 0,
    only_config: bool = False,
) -> int:
    """Run the function."""
    if multirun:
        hydra_args = ["hydra.mode=MULTIRUN", *list(hydra_args)]
    configs = get_hydra_configs(config_file, hydra_args)
    if only_config:
        function = partial(display_config, logger=_logger)

    if parallel:
        _logger.info("Running in parallel mode")
        return _run_parallel(function, configs, num_shards=num_shards)
    _logger.info("Running in sequential mode")
    return _run_sequential(function, configs, num_shards=num_shards)
