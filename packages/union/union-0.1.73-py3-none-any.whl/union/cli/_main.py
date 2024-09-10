from flytekit.clis.sdk_in_container.pyflyte import main as pyflyte_main

from union._config import _UNION_CONFIG
from union._usage import _configure_tracking_cli


def main(*args, **kwargs):
    """Main CLI entry point for directly calling `union`"""
    _UNION_CONFIG.is_direct_union_cli_call = True

    main = _configure_tracking_cli(pyflyte_main)
    return main(*args, **kwargs)
