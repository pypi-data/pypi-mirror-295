import configparser
import asyncio
import logging
import os
from pathlib import Path
import logging
from asyncinotify import Inotify, Mask
from syncservers.sync_server import SyncServer


logger = logging.getLogger(__name__)


def get_prefix(val):
    return f"{val}."


class Config:
    """
    define servers, path to servers mp
    reload config perodically
    refer to tests/syncservers/test_config.ini
    """

    SERVER_PREFIX = "server."
    SYNC_PATH_TYPES = ["live", "cron"]
    SYNC_PATH_PREFIXES = [get_prefix(val) for val in SYNC_PATH_TYPES]
    SPECIAL_PREFIXES = [SERVER_PREFIX] + SYNC_PATH_PREFIXES

    def __init__(self, config_file_path, delimiter='|') -> None:
        self._config_file_path = config_file_path
        self._delimiter = delimiter
        self._last_loaded_ts = 0

        self._servers = None
        self._path_type_mappings = None
        self._configs = None

    def get_config_file_path(self):
        return self._config_file_path

    def get_path_mappings(self, path_type):
        return self._path_type_mappings.get(path_type, {})

    def get_config(self, config_name):
        return self._configs.get(config_name, {})

    @staticmethod
    def get_boolean(config, key, default_value):
        return config[key].lower().strip() in ["true", "1"] if key in config else default_value

    @staticmethod
    def get_split_list(config, key, delimiter, default_value):
        return [val.strip() for val in config[key].strip().split(delimiter)] if key in config else default_value

    def load_config(self):
        try:
            # check file timestamp
            ts = os.path.getmtime(self._config_file_path)
            if ts == self._last_loaded_ts:
                logger.info("skipping loading configs because file is not changed according to mttime {ts}")
                return

            logger.info(f"loading configs from {self._config_file_path}")
            c = configparser.ConfigParser()
            c.read(self._config_file_path)

            # servers
            servers = self._load_servers(c, self.SERVER_PREFIX)

            # paths
            path_type_mappings = {}
            for path_type in self.SYNC_PATH_TYPES:
                path_mappings = self._load_path_mappings(
                    c, get_prefix(path_type), servers, self.SERVER_PREFIX
                )
                if path_mappings:
                    path_type_mappings[path_type] = path_mappings

            # other configs
            configs = self._load_configs(c, self.SPECIAL_PREFIXES)

            self._verify_config(servers, path_type_mappings, configs)

            self._servers = servers
            self._path_type_mappings = path_type_mappings
            self._configs = configs

            self._last_loaded_ts = ts

            return True
        except Exception as ex:
            logger.info("error in run_task", ex)
            return False

    def _verify_config(self, servers, path_type_mappings, configs):
        # must have servers
        if not servers:
            raise Exception("must have server. sections")

        # live and cron must at least have one
        if all([path_type not in path_type_mappings for path_type in self.SYNC_PATH_TYPES]):
            raise Exception("must have live or cron mappings config section")

    def _load_configs(self, c, excluded_prefixes):
        configs = {}
        for section in c.sections():
            # add not excluded configs
            if all([not section.startswith(prefix) for prefix in excluded_prefixes]):
                configs[section] = dict(c[section])
        return configs

    def _load_servers(self, c, prefix):
        prefix_len = len(prefix)
        servers = {}
        for section in c.sections():
            if section.startswith(prefix):
                server_id = section[prefix_len:]
                kwargs = dict(c[section].items())
                servers[server_id] = SyncServer(server_id=server_id, **kwargs)
        return servers

    def _load_path_mappings(self, c, prefix, servers, server_prefix):
        """
        result format:
        {
            "path1": (
                {"path_config_key1": "value1", ...},
                [
                    (sync_server1, param1, param2, ...),
                    (sync_server2, param1, param2, ...),
                    ...
                ]
            )
            "path2": ...
        }
        """
        prefix_len = len(prefix)
        server_prefix_len =  len(server_prefix)
        path_mappings = {}
        for section in c.sections():
            if section.startswith(prefix):
                path = os.path.normpath(section[prefix_len:].strip())
                path_configs = {}
                server_list = []
                for key, value in c[section].items():
                    if key.startswith(server_prefix):
                        # server list
                        server_id = key[server_prefix_len:]
                        server_list.append(tuple(
                            [servers[server_id]] + [val_str.strip() for val_str in value.split(self._delimiter)]
                        ))
                    else:
                        # config values
                        path_configs[key] = value

                path_mappings[path] = (path_configs, server_list)
        return path_mappings


class ConfigSync:
    """
    monitor config file change and reload configs
    """

    def __init__(self, config) -> None:
        self._config = config
        config_file_path = config.get_config_file_path()
        self._config_folder_path = os.path.dirname(config_file_path)
        self._config_file_path = config_file_path

    def run(self):
        return asyncio.create_task(self._watch_config())

    async def _watch_config(self):
        config_file_path = Path(self._config_file_path)
        with Inotify() as inotify:
            logger.info(f"watching config folder: {self._config_folder_path}")
            inotify.add_watch(self._config_folder_path, Mask.MOVED_TO | Mask.CLOSE_WRITE)
            async for event in inotify:
                if not event.mask & Mask.ISDIR and event.path == config_file_path:
                    logger.info(f"config file changed, reloading {str(config_file_path)}")
                    self._config.load_config()
