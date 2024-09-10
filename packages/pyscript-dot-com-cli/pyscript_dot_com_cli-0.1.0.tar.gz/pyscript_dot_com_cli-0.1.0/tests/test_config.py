from pathlib import Path

from pyscript_dot_com.config import Settings

EXPECTED_CONFIG_VALUES = {
    "api_host": "https://pyscript.com",
    "api_base": "/api",
    "api_prefix": "/api/projects",
    "hidden_directory": ".pyscript.com",
    "manifest_path": ".pyscript.com/manifest.json",
    "ignore": set(),
    "archive_ignore": {".*", "*.pyc"},
    "archive_name": "archive",
    "archive_format": "zip",
}


def test_default_config():
    """
    Test the default configuration asserting it has the expected values
    """
    # given a configuration without any file to load from
    settings = Settings(_env_file=None)

    # expect that it matches the main config and that both match the
    # default values
    # ensure that everything else match the default values
    for k, v in EXPECTED_CONFIG_VALUES.items():
        assert getattr(settings, k) == v


def test_config_global(global_config, global_config_values):
    """
    Test configuration loading custom values from a global config folder
    """
    # given a configuration loading values from a global config that exists
    # and a local that doesn't
    settings = Settings(_env_file=(global_config, Path("nowhere")))

    # ensure that the custom values match what was in the config file
    for k, v in global_config_values.items():
        assert getattr(settings, k) == v

    # ensure that everything else match the default values
    for k, v in EXPECTED_CONFIG_VALUES.items():
        if k not in global_config_values:
            assert getattr(settings, k) == v


def test_config_local(local_config, local_config_values):
    """
    Test configuration loading custom values from a local config folder
    """
    # given a configuration loading values from a local config that exists
    # and a global that doesn't
    settings = Settings(_env_file=(Path("nowhere"), local_config))

    # ensure that the custom values match what was in the config file
    for k, v in local_config_values.items():
        assert getattr(settings, k) == v

    # ensure that everything else match the default values
    for k, v in EXPECTED_CONFIG_VALUES.items():
        if k not in local_config_values:
            assert getattr(settings, k) == v


def test_config_local_and_global(
    local_config, local_config_values, global_config, global_config_values
):
    """
    Test configuration loading custom values from a local config folder
    """
    # given a configuration loading values from a global config
    # and a local that exist
    settings = Settings(_env_file=(global_config, local_config))

    # ensure that the custom values match what was in the config file
    for k, v in local_config_values.items():
        assert getattr(settings, k) == v

    # ensure that the custom values match what was in the config file
    for k, v in global_config_values.items():
        # making sure that we skip the keys that were in the local config
        # since that should take precedence over global
        if k not in local_config_values:
            assert getattr(settings, k) == v

    # ensure that everything else match the default values
    all_keys = set(global_config_values).union(local_config_values)
    for k, v in EXPECTED_CONFIG_VALUES.items():
        if k not in all_keys:
            assert getattr(settings, k) == v


def test_config_w_ignore_global(global_ignore, global_ignore_list):
    """
    Test configuration loading custom values from a global config folder
    """
    # given a file listing the things to ignore (as the fixtures as arguments)

    # and that the configuration file is passed to the config
    settings = Settings(_env_file=None, ignore=set(), global_ignore_path=global_ignore)

    # ensure that the ignore list matches what we set
    assert settings.ignore == global_ignore_list

    # and all the other values match the default
    for k, v in EXPECTED_CONFIG_VALUES.items():
        if k != "ignore":
            assert getattr(settings, k) == v


def test_config_w_ignore_local(local_ignore, local_ignore_list):
    """
    Test configuration loading custom values from a local config folder
    """
    # given a file listing the things to ignore (as the fixtures as arguments)

    # and that the configuration file is passed to the config
    settings = Settings(_env_file=None, ignore=set(), local_ignore_path=local_ignore)

    # ensure that the ignore list matches what we set
    assert settings.ignore == local_ignore_list

    # and all the other values match the default
    for k, v in EXPECTED_CONFIG_VALUES.items():
        if k != "ignore":
            assert getattr(settings, k) == v


def test_config_w_ignore(
    global_ignore, global_ignore_list, local_ignore, local_ignore_list
):
    """
    Test configuration loading custom values from a global and a local config folder
    """
    # given a file listing the things to ignore (as the fixtures as arguments)

    # and that the configuration file is passed to the config
    settings = Settings(
        _env_file=None,
        ignore=set(),
        global_ignore_path=global_ignore,
        local_ignore_path=local_ignore,
    )

    # ensure that the ignore list matches what we set
    assert settings.ignore == local_ignore_list.union(global_ignore_list)

    # and all the other values match the default
    for k, v in EXPECTED_CONFIG_VALUES.items():
        if k != "ignore":
            assert getattr(settings, k) == v


def test_config_w_ignore_local_and_global(
    local_config,
    local_config_values,
    global_config,
    global_config_values,
    global_ignore,
    global_ignore_list,
    local_ignore,
    local_ignore_list,
):
    """
    Test configuration loading custom values from a global and a local config folder
    """
    # given a file listing the things to ignore (as the fixtures as arguments)
    # and a configuration loading values from a global config
    # and a local that exist
    settings = Settings(
        _env_file=(global_config, local_config),
        ignore=set(),
        global_ignore_path=global_ignore,
        local_ignore_path=local_ignore,
    )

    # ensure that the ignore list matches what we set
    assert settings.ignore == local_ignore_list.union(global_ignore_list)

    # ensure that the custom values match what was in the config file
    for k, v in local_config_values.items():
        assert getattr(settings, k) == v

    # ensure that the custom values match what was in the config file
    for k, v in global_config_values.items():
        # making sure that we skip the keys that were in the local config
        # since that should take precedence over global
        if k not in local_config_values:
            assert getattr(settings, k) == v

    # ensure that everything else match the default values
    all_keys = (
        set(global_config_values)
        .union(local_config_values)
        .union(
            {
                "ignore",
            }
        )
    )
    for k, v in EXPECTED_CONFIG_VALUES.items():
        if k not in all_keys:
            assert getattr(settings, k) == v
