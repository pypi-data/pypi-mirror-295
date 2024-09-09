# Copyright
# Extended by Advantch.com 2023
# Attribution: Modal Labs 2022
import logging
import os
import typing
import warnings
import toml

# Locate config file and read it

user_config_path: str = os.environ.get("VANTY_CONFIG_PATH") or os.path.expanduser(
    "~/.vanty.toml"
)


def _read_user_config():
    # first check the current directory
    base = {}
    extended = {}
    cwd = os.getcwd()
    if os.path.exists(f"{cwd}/vanty.toml"):
        with open(f"{cwd}/vanty.toml") as f:
            try:
                base = toml.load(f)
            except toml.TomlDecodeError:
                pass
    # then check the user config path
    if os.path.exists(user_config_path):
        with open(user_config_path) as f:
            try:
                extended = toml.load(f)
            except toml.TomlDecodeError:
                pass
    print(base, extended, "user_config")
    return {**base, **extended}


_user_config = _read_user_config()


def config_profiles():
    """List the available vanty profiles in the .vanty.toml file."""
    return _user_config.keys()


def _config_active_profile():
    for key, values in _user_config.items():
        if values.get("active", False) is True:
            return key
    else:
        return "default"


def _store_user_config(new_settings, profile="default"):
    """Internal method, used by the CLI to set tokens."""
    if profile is None:
        profile = _profile
    user_config = _read_user_config()
    user_config.setdefault(profile, {}).update(**new_settings)
    _write_user_config(user_config)


def _write_user_config(user_config):
    with open(user_config_path, "w") as f:
        toml.dump(user_config, f)


def config_set_active_profile(env: str):
    """Set the user's active vanty profile by writing it to the `.vanty.toml` file."""
    if env not in _user_config:
        raise KeyError(env)

    for key, values in _user_config.items():
        values.pop("active", None)

    _user_config[env]["active"] = True
    _write_user_config(_user_config)


_profile = os.environ.get("VANTY_PROFILE", _config_active_profile())


class _Setting(typing.NamedTuple):
    default: typing.Any = None
    transform: typing.Callable[[str], typing.Any] = lambda x: x  # noqa: E731


_SETTINGS = {
    "loglevel": _Setting("WARNING", lambda s: s.upper()),
    "server_url": _Setting(default="https://www.advantch.com/api/v1"),
    "token_id": _Setting(),
    "local_folder": _Setting(default=".", transform=os.path.abspath),
    "token_secret": _Setting(),
    "ssr_enabled": _Setting(default=False, transform=lambda s: s.lower() == "true"),
    "package_manager": _Setting(default="pnpm"),
    "frontend_root": _Setting(default="."),
    "core_service_name": _Setting(default="django"),
    "worker_service_name": _Setting(default="worker"),
    "cache_service_name": _Setting(default="redis"),
    "use_docker": _Setting(default=True),  # update for non docker
}


class Config:
    """Singleton that holds configuration used by Vanty internally."""

    def __init__(self):
        pass

    def get(self, key, profile="default"):
        """Looks up a configuration value.

        Will check (in decreasing order of priority):
        1. Any environment variable of the form VANTY_FOO_BAR
        2. Settings in the user's .toml configuration file
        3. Local .toml file in the current directory
        4. The default value of the setting
        """
        if profile is None:
            profile = _profile
        s = _SETTINGS[key]
        env_var_key = "VANTY_" + key.upper()
        _user_config = _read_user_config()
        _user_config.get(profile, {})

        if env_var_key in os.environ:
            return s.transform(os.environ[env_var_key])
        elif profile in _user_config and key in _user_config[profile]:
            return s.transform(_user_config[profile][key])
        else:
            return s.default

    def __getitem__(self, key):
        return self.get(key)

    def display(self):
        return {key: self.get(key) for key in _SETTINGS.keys()}

    @property
    def active_config(self):
        return _profile

    @property
    def user_config(self):
        return _read_user_config()

    def set_active_config(self, profile):
        _profile = profile

    def __repr__(self):
        return repr({key: self.get(key) for key in _SETTINGS.keys()})


config = Config()

# Logging

logger = logging.getLogger("vanty-cli")
ch = logging.StreamHandler()
log_level_numeric = logging.getLevelName(config["loglevel"])
logger.setLevel(log_level_numeric)
ch.setLevel(log_level_numeric)
ch.setFormatter(
    logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z")
)
logger.addHandler(ch)

# Utils to write config


# Make sure all deprecation warnings are shown
# See https://docs.python.org/3/library/warnings.html#overriding-the-default-filter
warnings.filterwarnings(
    "default",
    category=DeprecationWarning,
    module="vanty",
)
