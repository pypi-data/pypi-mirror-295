import hashlib
import json
import logging
from typing import Any

from omegaconf import DictConfig, OmegaConf

_logger = logging.getLogger(__name__)


def hash_dict(data: dict[str, Any]) -> str:
    """Return a hash of a dictionary."""
    string = json.dumps(data, indent=True, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(string.encode()).hexdigest()


def hash_config(cfg: DictConfig) -> str:
    """Compute a unique identifier that summarizes the provided config."""
    if isinstance(cfg, DictConfig):
        config_dict: dict = OmegaConf.to_container(cfg, resolve=True)  # type: ignore
    else:
        config_dict = dict(cfg)
    return hash_dict(config_dict)


def display_config(config: DictConfig = None, logger=None, **kwargs) -> int:
    """Display the configuration."""
    try:
        config_uuid = hash_config(config)
    except Exception as e:
        if logger:
            logger.error(f"Error hashing config {config}: {e}")
        config_uuid = None
    if logger:
        logger.info(f"Loaded config with uuid {config_uuid}")
    if kwargs:
        logger.warning("The configuration is a dictionary, not a DictConfig object.")
        if config is not None:
            kwargs["config"] = config
        to_print = json.dumps(kwargs, indent=4)
        if logger:
            logger.info(f"Config values:\n{to_print}")
        return 0

    try:
        to_print = json.dumps(OmegaConf.to_container(config, resolve=True), indent=4)
        if logger:
            logger.info(f"Config values:\n{to_print}")
    except Exception as e:
        if logger:
            logger.error(f"Error resolving config: {e}")
        try:
            to_print = json.dumps(OmegaConf.to_container(config), indent=4)
            if logger:
                logger.info(f"Config values:\n{to_print}")
        except Exception as e:
            if logger:
                logger.error(f"Error printing config: {e}")
                logger.info(f"Config values:\n{config}")
        return 1

    return 0
